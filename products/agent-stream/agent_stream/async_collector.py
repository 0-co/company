"""
AsyncStreamCollector: async streaming LLM response handling.
"""

import asyncio
import time
from typing import Any, Callable, Coroutine, Dict, List, Optional

from .collector import StreamError, StreamResult


class AsyncStreamCollector:
    """
    Async version of StreamCollector. Handles Anthropic and OpenAI async streams.

    Parameters
    ----------
    on_chunk:
        Optional async or sync callback called with each text chunk.
        Signature: fn(text: str) -> None  OR  async fn(text: str) -> None
    capture_chunks:
        Whether to store individual chunks in StreamResult.chunks.
    cancel_event:
        Optional asyncio.Event. Set it to stop the stream mid-way.
    """

    def __init__(
        self,
        on_chunk: Optional[Callable] = None,
        capture_chunks: bool = True,
        cancel_event: Optional[asyncio.Event] = None,
    ):
        self.on_chunk = on_chunk
        self.capture_chunks = capture_chunks
        self.cancel_event = cancel_event

    async def _call_on_chunk(self, text: str) -> None:
        if not self.on_chunk:
            return
        result = self.on_chunk(text)
        if asyncio.iscoroutine(result):
            await result

    # ------------------------------------------------------------------
    # Anthropic async streaming

    async def collect_anthropic(self, stream) -> StreamResult:
        """
        Collect an Anthropic async streaming context manager response.

        Usage::

            async with client.messages.stream(...) as stream:
                result = await collector.collect_anthropic(stream)
        """
        result = StreamResult()
        start = time.monotonic()

        try:
            async for event in stream:
                if self.cancel_event and self.cancel_event.is_set():
                    result.stop_reason = "cancelled"
                    break

                event_type = getattr(event, "type", None)

                if event_type == "content_block_delta":
                    delta = getattr(event, "delta", None)
                    if delta and getattr(delta, "type", None) == "text_delta":
                        chunk = getattr(delta, "text", "")
                        result.text += chunk
                        if self.capture_chunks:
                            result.chunks.append(chunk)
                        await self._call_on_chunk(chunk)

                elif event_type == "message_start":
                    msg = getattr(event, "message", None)
                    if msg:
                        usage = getattr(msg, "usage", None)
                        if usage:
                            result.input_tokens = getattr(usage, "input_tokens", 0)
                        result.model = getattr(msg, "model", "")

                elif event_type == "message_delta":
                    usage = getattr(event, "usage", None)
                    if usage:
                        result.output_tokens = getattr(usage, "output_tokens", 0)
                    delta = getattr(event, "delta", None)
                    if delta:
                        result.stop_reason = getattr(delta, "stop_reason", "") or ""

        except Exception as e:
            raise StreamError(f"Anthropic async stream failed: {e}") from e

        result.duration_ms = (time.monotonic() - start) * 1000
        return result

    async def stream_anthropic(self, client, **kwargs) -> StreamResult:
        """Open an Anthropic async stream, collect it, return StreamResult."""
        try:
            async with client.messages.stream(**kwargs) as stream:
                return await self.collect_anthropic(stream)
        except StreamError:
            raise
        except Exception as e:
            raise StreamError(f"Failed to start Anthropic async stream: {e}") from e

    # ------------------------------------------------------------------
    # OpenAI async streaming

    async def collect_openai(self, stream) -> StreamResult:
        """
        Collect an OpenAI async streaming response.

        Usage::

            stream = await client.chat.completions.create(..., stream=True)
            result = await collector.collect_openai(stream)
        """
        result = StreamResult()
        start = time.monotonic()

        try:
            async for chunk in stream:
                if self.cancel_event and self.cancel_event.is_set():
                    result.stop_reason = "cancelled"
                    break

                if not result.model:
                    result.model = getattr(chunk, "model", "")

                choices = getattr(chunk, "choices", [])
                for choice in choices:
                    delta = getattr(choice, "delta", None)
                    if delta:
                        text = getattr(delta, "content", None) or ""
                        if text:
                            result.text += text
                            if self.capture_chunks:
                                result.chunks.append(text)
                            await self._call_on_chunk(text)

                    finish_reason = getattr(choice, "finish_reason", None)
                    if finish_reason:
                        result.stop_reason = finish_reason

                usage = getattr(chunk, "usage", None)
                if usage:
                    result.input_tokens = getattr(usage, "prompt_tokens", 0)
                    result.output_tokens = getattr(usage, "completion_tokens", 0)

        except Exception as e:
            raise StreamError(f"OpenAI async stream failed: {e}") from e

        result.duration_ms = (time.monotonic() - start) * 1000
        return result

    async def stream_openai(self, client, **kwargs) -> StreamResult:
        """Open an OpenAI async stream, collect it, return StreamResult."""
        kwargs["stream"] = True
        try:
            stream = await client.chat.completions.create(**kwargs)
            return await self.collect_openai(stream)
        except StreamError:
            raise
        except Exception as e:
            raise StreamError(f"Failed to start OpenAI async stream: {e}") from e
