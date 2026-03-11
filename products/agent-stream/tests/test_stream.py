"""
Tests for agent-stream.
"""

import asyncio
import threading
import time
import unittest
from unittest.mock import MagicMock

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_stream import StreamCollector, StreamResult, StreamError, AsyncStreamCollector


# ---------------------------------------------------------------------------
# Mock stream helpers

def make_anthropic_events(text: str, input_tokens: int = 10, output_tokens: int = 20):
    """Generate a sequence of mock Anthropic streaming events."""
    # message_start
    msg_start = MagicMock()
    msg_start.type = "message_start"
    msg_start.message = MagicMock()
    msg_start.message.usage = MagicMock()
    msg_start.message.usage.input_tokens = input_tokens
    msg_start.message.model = "claude-haiku-4-5"
    yield msg_start

    # content_block_delta for each character
    for char in text:
        event = MagicMock()
        event.type = "content_block_delta"
        event.delta = MagicMock()
        event.delta.type = "text_delta"
        event.delta.text = char
        yield event

    # message_delta with usage and stop_reason
    msg_delta = MagicMock()
    msg_delta.type = "message_delta"
    msg_delta.usage = MagicMock()
    msg_delta.usage.output_tokens = output_tokens
    msg_delta.delta = MagicMock()
    msg_delta.delta.stop_reason = "end_turn"
    yield msg_delta


def make_openai_chunks(text: str, input_tokens: int = 10, output_tokens: int = 20):
    """Generate a sequence of mock OpenAI streaming chunks."""
    for i, char in enumerate(text):
        chunk = MagicMock()
        chunk.model = "gpt-4o"
        choice = MagicMock()
        choice.delta = MagicMock()
        choice.delta.content = char
        choice.finish_reason = None
        chunk.choices = [choice]
        chunk.usage = None
        yield chunk

    # Final chunk with stop reason and usage
    final = MagicMock()
    final.model = "gpt-4o"
    choice = MagicMock()
    choice.delta = MagicMock()
    choice.delta.content = None
    choice.finish_reason = "stop"
    final.choices = [choice]
    final.usage = MagicMock()
    final.usage.prompt_tokens = input_tokens
    final.usage.completion_tokens = output_tokens
    yield final


# Anthropic streaming context manager mock
class MockAnthropicStream:
    def __init__(self, events):
        self._events = list(events)

    def __iter__(self):
        return iter(self._events)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


# Async versions
class AsyncMockAnthropicStream:
    def __init__(self, events):
        self._events = list(events)

    def __aiter__(self):
        return self._async_iter()

    async def _async_iter(self):
        for e in self._events:
            yield e

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


class AsyncMockOpenAIStream:
    def __init__(self, chunks):
        self._chunks = list(chunks)

    def __aiter__(self):
        return self._async_iter()

    async def _async_iter(self):
        for c in self._chunks:
            yield c


# ---------------------------------------------------------------------------
# StreamResult tests

class TestStreamResult(unittest.TestCase):

    def test_defaults(self):
        r = StreamResult()
        self.assertEqual(r.text, "")
        self.assertEqual(r.input_tokens, 0)
        self.assertEqual(r.output_tokens, 0)
        self.assertEqual(r.stop_reason, "")
        self.assertEqual(r.chunks, [])

    def test_total_tokens(self):
        r = StreamResult(input_tokens=10, output_tokens=20)
        self.assertEqual(r.total_tokens, 30)

    def test_was_cancelled_true(self):
        r = StreamResult(stop_reason="cancelled")
        self.assertTrue(r.was_cancelled)

    def test_was_cancelled_false(self):
        r = StreamResult(stop_reason="end_turn")
        self.assertFalse(r.was_cancelled)

    def test_repr(self):
        r = StreamResult(text="Hello world", input_tokens=5, output_tokens=3, duration_ms=100.0)
        s = repr(r)
        self.assertIn("8", s)  # total_tokens
        self.assertIn("100", s)


# ---------------------------------------------------------------------------
# StreamCollector — Anthropic tests

class TestStreamCollectorAnthropic(unittest.TestCase):

    def _collect(self, text, input_tokens=10, output_tokens=20, **kwargs):
        collector = StreamCollector(**kwargs)
        stream = MockAnthropicStream(make_anthropic_events(text, input_tokens, output_tokens))
        return collector.collect_anthropic(stream)

    def test_collects_text(self):
        result = self._collect("Hello, world!")
        self.assertEqual(result.text, "Hello, world!")

    def test_input_tokens(self):
        result = self._collect("hi", input_tokens=15)
        self.assertEqual(result.input_tokens, 15)

    def test_output_tokens(self):
        result = self._collect("hi", output_tokens=5)
        self.assertEqual(result.output_tokens, 5)

    def test_stop_reason(self):
        result = self._collect("hi")
        self.assertEqual(result.stop_reason, "end_turn")

    def test_model(self):
        result = self._collect("hi")
        self.assertEqual(result.model, "claude-haiku-4-5")

    def test_duration_ms_positive(self):
        result = self._collect("hi")
        self.assertGreater(result.duration_ms, 0.0)

    def test_chunks_captured(self):
        result = self._collect("abc", capture_chunks=True)
        self.assertEqual(result.chunks, list("abc"))

    def test_chunks_not_captured(self):
        result = self._collect("abc", capture_chunks=False)
        self.assertEqual(result.chunks, [])

    def test_on_chunk_called(self):
        received = []
        result = self._collect("Hello", on_chunk=lambda t: received.append(t))
        self.assertEqual("".join(received), "Hello")

    def test_cancellation(self):
        cancel = threading.Event()
        cancel.set()  # already set before we start

        collector = StreamCollector(cancel_event=cancel)
        # Give it some events but it should cancel immediately
        events = list(make_anthropic_events("Hello world"))
        stream = MockAnthropicStream(events)
        result = collector.collect_anthropic(stream)
        self.assertTrue(result.was_cancelled)
        # Text may be empty or partial (cancelled before processing)
        self.assertIn(result.stop_reason, ["cancelled"])

    def test_empty_text(self):
        result = self._collect("")
        self.assertEqual(result.text, "")

    def test_long_text(self):
        long = "x" * 500
        result = self._collect(long)
        self.assertEqual(result.text, long)
        self.assertEqual(len(result.chunks), 500)


# ---------------------------------------------------------------------------
# StreamCollector — OpenAI tests

class TestStreamCollectorOpenAI(unittest.TestCase):

    def _collect(self, text, input_tokens=10, output_tokens=20, **kwargs):
        collector = StreamCollector(**kwargs)
        stream = make_openai_chunks(text, input_tokens, output_tokens)
        return collector.collect_openai(stream)

    def test_collects_text(self):
        result = self._collect("Hello, world!")
        self.assertEqual(result.text, "Hello, world!")

    def test_input_tokens(self):
        result = self._collect("hi", input_tokens=8)
        self.assertEqual(result.input_tokens, 8)

    def test_output_tokens(self):
        result = self._collect("hi", output_tokens=4)
        self.assertEqual(result.output_tokens, 4)

    def test_stop_reason(self):
        result = self._collect("hi")
        self.assertEqual(result.stop_reason, "stop")

    def test_model(self):
        result = self._collect("hi")
        self.assertEqual(result.model, "gpt-4o")

    def test_duration_ms_positive(self):
        result = self._collect("hi")
        self.assertGreater(result.duration_ms, 0.0)

    def test_chunks_captured(self):
        result = self._collect("abc", capture_chunks=True)
        self.assertEqual(result.chunks, list("abc"))

    def test_on_chunk_called(self):
        received = []
        result = self._collect("World", on_chunk=lambda t: received.append(t))
        self.assertEqual("".join(received), "World")

    def test_cancellation(self):
        cancel = threading.Event()
        cancel.set()
        collector = StreamCollector(cancel_event=cancel)
        stream = make_openai_chunks("Hello world")
        result = collector.collect_openai(stream)
        self.assertTrue(result.was_cancelled)

    def test_empty_text(self):
        result = self._collect("")
        self.assertEqual(result.text, "")


# ---------------------------------------------------------------------------
# StreamCollector — stream_anthropic / stream_openai wrappers

class TestStreamCollectorWrappers(unittest.TestCase):

    def test_stream_anthropic(self):
        mock_client = MagicMock()
        events = list(make_anthropic_events("Hello"))
        mock_client.messages.stream.return_value = MockAnthropicStream(events)

        collector = StreamCollector()
        result = collector.stream_anthropic(mock_client, model="claude-haiku-4-5", max_tokens=100)
        self.assertEqual(result.text, "Hello")

    def test_stream_anthropic_error(self):
        mock_client = MagicMock()
        mock_client.messages.stream.side_effect = Exception("network error")

        collector = StreamCollector()
        with self.assertRaises(StreamError) as ctx:
            collector.stream_anthropic(mock_client, model="claude-haiku-4-5")
        self.assertIn("network error", str(ctx.exception))

    def test_stream_openai_adds_stream_true(self):
        mock_client = MagicMock()
        chunks = list(make_openai_chunks("hi"))
        mock_client.chat.completions.create.return_value = iter(chunks)

        collector = StreamCollector()
        result = collector.stream_openai(mock_client, model="gpt-4o")
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        self.assertTrue(call_kwargs.get("stream"))

    def test_stream_openai_error(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = RuntimeError("timeout")

        collector = StreamCollector()
        with self.assertRaises(StreamError):
            collector.stream_openai(mock_client, model="gpt-4o")


# ---------------------------------------------------------------------------
# Async tests

class TestAsyncStreamCollector(unittest.IsolatedAsyncioTestCase):

    async def test_collect_anthropic(self):
        events = list(make_anthropic_events("Hello async"))
        stream = AsyncMockAnthropicStream(events)
        collector = AsyncStreamCollector()
        result = await collector.collect_anthropic(stream)
        self.assertEqual(result.text, "Hello async")

    async def test_collect_anthropic_tokens(self):
        events = list(make_anthropic_events("hi", input_tokens=7, output_tokens=3))
        stream = AsyncMockAnthropicStream(events)
        collector = AsyncStreamCollector()
        result = await collector.collect_anthropic(stream)
        self.assertEqual(result.input_tokens, 7)
        self.assertEqual(result.output_tokens, 3)

    async def test_collect_openai(self):
        chunks = list(make_openai_chunks("Async OpenAI"))
        stream = AsyncMockOpenAIStream(chunks)
        collector = AsyncStreamCollector()
        result = await collector.collect_openai(stream)
        self.assertEqual(result.text, "Async OpenAI")

    async def test_on_chunk_sync_callback(self):
        received = []
        events = list(make_anthropic_events("abc"))
        stream = AsyncMockAnthropicStream(events)
        collector = AsyncStreamCollector(on_chunk=lambda t: received.append(t))
        await collector.collect_anthropic(stream)
        self.assertEqual("".join(received), "abc")

    async def test_on_chunk_async_callback(self):
        received = []

        async def async_on_chunk(text):
            received.append(text)

        events = list(make_anthropic_events("xyz"))
        stream = AsyncMockAnthropicStream(events)
        collector = AsyncStreamCollector(on_chunk=async_on_chunk)
        await collector.collect_anthropic(stream)
        self.assertEqual("".join(received), "xyz")

    async def test_cancellation_anthropic(self):
        cancel = asyncio.Event()
        cancel.set()
        events = list(make_anthropic_events("long text here"))
        stream = AsyncMockAnthropicStream(events)
        collector = AsyncStreamCollector(cancel_event=cancel)
        result = await collector.collect_anthropic(stream)
        self.assertTrue(result.was_cancelled)

    async def test_cancellation_openai(self):
        cancel = asyncio.Event()
        cancel.set()
        chunks = list(make_openai_chunks("some text"))
        stream = AsyncMockOpenAIStream(chunks)
        collector = AsyncStreamCollector(cancel_event=cancel)
        result = await collector.collect_openai(stream)
        self.assertTrue(result.was_cancelled)

    async def test_capture_chunks_false(self):
        events = list(make_anthropic_events("abc"))
        stream = AsyncMockAnthropicStream(events)
        collector = AsyncStreamCollector(capture_chunks=False)
        result = await collector.collect_anthropic(stream)
        self.assertEqual(result.chunks, [])
        self.assertEqual(result.text, "abc")

    async def test_stream_anthropic_wrapper(self):
        mock_client = MagicMock()
        events = list(make_anthropic_events("Async hello"))
        mock_client.messages.stream.return_value = AsyncMockAnthropicStream(events)

        collector = AsyncStreamCollector()
        result = await collector.stream_anthropic(mock_client, model="claude-haiku-4-5", max_tokens=50)
        self.assertEqual(result.text, "Async hello")

    async def test_stream_anthropic_error(self):
        mock_client = MagicMock()
        mock_client.messages.stream.side_effect = Exception("async network error")

        collector = AsyncStreamCollector()
        with self.assertRaises(StreamError) as ctx:
            await collector.stream_anthropic(mock_client, model="claude-haiku-4-5")
        self.assertIn("async network error", str(ctx.exception))


# ---------------------------------------------------------------------------
# StreamError tests

class TestStreamError(unittest.TestCase):

    def test_is_exception(self):
        e = StreamError("something went wrong")
        self.assertIsInstance(e, Exception)

    def test_message(self):
        e = StreamError("oops")
        self.assertEqual(str(e), "oops")


if __name__ == "__main__":
    unittest.main()
