"""
StreamCollector: synchronous streaming LLM response handling.

Handles the messy parts of streaming:
- Collecting chunks into a complete response
- Tracking input/output token counts as they arrive
- Cancellation support (stop mid-stream)
- on_chunk callbacks for real-time display
- Normalizes Anthropic and OpenAI streaming formats

Usage::

    from agent_stream import StreamCollector

    collector = StreamCollector(
        on_chunk=lambda text: print(text, end="", flush=True)
    )

    with collector.stream(client, model="claude-sonnet-4-6", messages=[...]) as result:
        print()  # newline after streaming completes
        print(result.text)         # complete response
        print(result.input_tokens) # tokens used
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


class StreamError(Exception):
    """Raised when a streaming operation fails."""
    pass


@dataclass
class StreamResult:
    """
    The complete result of a streaming LLM call.

    Attributes
    ----------
    text:
        Full response text assembled from all chunks.
    input_tokens:
        Number of input tokens (from API usage data).
    output_tokens:
        Number of output tokens (from API usage data).
    stop_reason:
        Why generation stopped ('end_turn', 'max_tokens', 'cancelled', etc.)
    duration_ms:
        Wall-clock time from first chunk to last chunk.
    model:
        Model name used for this generation.
    chunks:
        Individual text chunks in order (if captured).
    metadata:
        Provider-specific metadata (e.g. model version, finish_reason).
    """

    text: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    stop_reason: str = ""
    duration_ms: float = 0.0
    model: str = ""
    chunks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def was_cancelled(self) -> bool:
        return self.stop_reason == "cancelled"

    def __repr__(self) -> str:
        preview = self.text[:60] + "..." if len(self.text) > 60 else self.text
        return (
            f"StreamResult(tokens={self.total_tokens}, "
            f"duration={self.duration_ms:.0f}ms, "
            f"text={preview!r})"
        )


class StreamCollector:
    """
    Collects a streaming LLM response into a StreamResult.
    Handles Anthropic and OpenAI streaming protocols.

    Parameters
    ----------
    on_chunk:
        Optional callback called with each text chunk as it arrives.
        Signature: fn(text: str) -> None
        Use this to display text in real-time.
    capture_chunks:
        Whether to store individual chunks in StreamResult.chunks.
        Default True. Set to False for lower memory usage on long responses.
    cancel_event:
        Optional threading.Event. Set it to stop the stream mid-way.
        The result will have stop_reason='cancelled'.
    """

    def __init__(
        self,
        on_chunk: Optional[Callable[[str], None]] = None,
        capture_chunks: bool = True,
        cancel_event: Optional[threading.Event] = None,
    ):
        self.on_chunk = on_chunk
        self.capture_chunks = capture_chunks
        self.cancel_event = cancel_event

    # ------------------------------------------------------------------
    # Anthropic streaming

    def collect_anthropic(self, stream) -> StreamResult:
        """
        Collect an Anthropic streaming context manager response.

        Usage::

            with client.messages.stream(...) as stream:
                result = collector.collect_anthropic(stream)
        """
        result = StreamResult()
        start = time.monotonic()

        try:
            for event in stream:
                if self.cancel_event and self.cancel_event.is_set():
                    result.stop_reason = "cancelled"
                    break

                event_type = getattr(event, "type", None)

                # Text delta
                if event_type == "content_block_delta":
                    delta = getattr(event, "delta", None)
                    if delta and getattr(delta, "type", None) == "text_delta":
                        chunk = getattr(delta, "text", "")
                        result.text += chunk
                        if self.capture_chunks:
                            result.chunks.append(chunk)
                        if self.on_chunk:
                            self.on_chunk(chunk)

                # Usage info (arrives in message_delta or message_start)
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
            raise StreamError(f"Anthropic stream failed: {e}") from e

        result.duration_ms = (time.monotonic() - start) * 1000
        return result

    def stream_anthropic(self, client, **kwargs) -> StreamResult:
        """
        Open an Anthropic streaming call, collect it, and return StreamResult.

        Example::

            result = collector.stream_anthropic(
                client,
                model="claude-sonnet-4-6",
                max_tokens=500,
                messages=[{"role": "user", "content": "Hello"}],
            )
        """
        try:
            with client.messages.stream(**kwargs) as stream:
                return self.collect_anthropic(stream)
        except StreamError:
            raise
        except Exception as e:
            raise StreamError(f"Failed to start Anthropic stream: {e}") from e

    # ------------------------------------------------------------------
    # OpenAI streaming

    def collect_openai(self, stream) -> StreamResult:
        """
        Collect an OpenAI streaming response iterator.

        Usage::

            stream = client.chat.completions.create(..., stream=True)
            result = collector.collect_openai(stream)
        """
        result = StreamResult()
        start = time.monotonic()

        try:
            for chunk in stream:
                if self.cancel_event and self.cancel_event.is_set():
                    result.stop_reason = "cancelled"
                    break

                # Model name (from first chunk)
                if not result.model:
                    result.model = getattr(chunk, "model", "")

                choices = getattr(chunk, "choices", [])
                for choice in choices:
                    # Text delta
                    delta = getattr(choice, "delta", None)
                    if delta:
                        text = getattr(delta, "content", None) or ""
                        if text:
                            result.text += text
                            if self.capture_chunks:
                                result.chunks.append(text)
                            if self.on_chunk:
                                self.on_chunk(text)

                    # Stop reason
                    finish_reason = getattr(choice, "finish_reason", None)
                    if finish_reason:
                        result.stop_reason = finish_reason

                # Usage (OpenAI sends at the end as a special chunk)
                usage = getattr(chunk, "usage", None)
                if usage:
                    result.input_tokens = getattr(usage, "prompt_tokens", 0)
                    result.output_tokens = getattr(usage, "completion_tokens", 0)

        except Exception as e:
            raise StreamError(f"OpenAI stream failed: {e}") from e

        result.duration_ms = (time.monotonic() - start) * 1000
        return result

    def stream_openai(self, client, **kwargs) -> StreamResult:
        """
        Open an OpenAI streaming call, collect it, and return StreamResult.

        Example::

            result = collector.stream_openai(
                client,
                model="gpt-4o",
                stream=True,
                messages=[{"role": "user", "content": "Hello"}],
            )
        """
        kwargs["stream"] = True
        try:
            stream = client.chat.completions.create(**kwargs)
            return self.collect_openai(stream)
        except StreamError:
            raise
        except Exception as e:
            raise StreamError(f"Failed to start OpenAI stream: {e}") from e
