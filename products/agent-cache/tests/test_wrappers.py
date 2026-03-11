"""Tests for Anthropic and OpenAI client wrappers."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_cache import ResponseCache
from agent_cache.wrappers import CachedAnthropicClient, CachedOpenAIClient


# ---------------------------------------------------------------------------
# Fake SDK clients
# ---------------------------------------------------------------------------

class FakeMessages:
    def __init__(self):
        self.call_count = 0

    def create(self, model, messages, **kwargs):
        self.call_count += 1
        return {
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "model": model,
            "content": [{"type": "text", "text": f"response {self.call_count}"}],
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 10, "output_tokens": 5},
        }

    def some_other_method(self):
        return "passthrough"


class FakeAnthropicClient:
    __module__ = "anthropic"

    def __init__(self):
        self.messages = FakeMessages()
        self.api_key = "sk-test"


class FakeCompletions:
    def __init__(self):
        self.call_count = 0

    def create(self, model, messages, **kwargs):
        self.call_count += 1
        if kwargs.get("stream"):
            return iter([])
        return {
            "id": "chatcmpl_test",
            "object": "chat.completion",
            "model": model,
            "choices": [{"message": {"role": "assistant", "content": f"response {self.call_count}"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }


class FakeChat:
    def __init__(self):
        self.completions = FakeCompletions()


class FakeOpenAIClient:
    __module__ = "openai"

    def __init__(self):
        self.chat = FakeChat()
        self.api_key = "sk-test"


# ---------------------------------------------------------------------------
# Anthropic wrapper tests
# ---------------------------------------------------------------------------

class TestCachedAnthropicClient(unittest.TestCase):
    def _make(self):
        cache = ResponseCache(path=tempfile.mktemp(suffix=".json"))
        real = FakeAnthropicClient()
        wrapped = CachedAnthropicClient(real, cache)
        return wrapped, real, cache

    def test_first_call_hits_api(self):
        wrapped, real, _ = self._make()
        wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hi"}],
        )
        self.assertEqual(real.messages.call_count, 1)

    def test_second_call_uses_cache(self):
        wrapped, real, _ = self._make()
        r1 = wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hi"}],
        )
        r2 = wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hi"}],
        )
        self.assertEqual(real.messages.call_count, 1)

    def test_different_messages_call_api_again(self):
        wrapped, real, _ = self._make()
        wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hi"}],
        )
        wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "different question"}],
        )
        self.assertEqual(real.messages.call_count, 2)

    def test_passthrough_attributes(self):
        wrapped, real, _ = self._make()
        self.assertEqual(wrapped.api_key, "sk-test")

    def test_messages_passthrough_attributes(self):
        wrapped, real, _ = self._make()
        self.assertEqual(wrapped.messages.some_other_method(), "passthrough")

    def test_cached_response_attribute_access(self):
        wrapped, _, _ = self._make()
        r1 = wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hi"}],
        )
        r2 = wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hi"}],
        )
        # r2 comes from cache — should still work as namespace
        self.assertEqual(r2.content[0].text, "response 1")

    def test_repr(self):
        wrapped, _, _ = self._make()
        self.assertIn("CachedAnthropicClient", repr(wrapped))

    def test_cache_stats(self):
        wrapped, _, cache = self._make()
        wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "x"}],
        )
        wrapped.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "x"}],
        )
        s = cache.stats()
        self.assertEqual(s.hits, 1)
        self.assertEqual(s.misses, 1)


# ---------------------------------------------------------------------------
# OpenAI wrapper tests
# ---------------------------------------------------------------------------

class TestCachedOpenAIClient(unittest.TestCase):
    def _make(self):
        cache = ResponseCache(path=tempfile.mktemp(suffix=".json"))
        real = FakeOpenAIClient()
        wrapped = CachedOpenAIClient(real, cache)
        return wrapped, real, cache

    def test_first_call_hits_api(self):
        wrapped, real, _ = self._make()
        wrapped.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "hello"}],
        )
        self.assertEqual(real.chat.completions.call_count, 1)

    def test_second_call_cached(self):
        wrapped, real, _ = self._make()
        for _ in range(3):
            wrapped.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "hello"}],
            )
        self.assertEqual(real.chat.completions.call_count, 1)

    def test_streaming_not_cached(self):
        wrapped, real, _ = self._make()
        for _ in range(2):
            wrapped.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "hello"}],
                stream=True,
            )
        # streaming bypasses cache — both calls hit API
        self.assertEqual(real.chat.completions.call_count, 2)

    def test_passthrough_attributes(self):
        wrapped, real, _ = self._make()
        self.assertEqual(wrapped.api_key, "sk-test")

    def test_cached_response_has_content(self):
        wrapped, _, _ = self._make()
        wrapped.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "q"}],
        )
        r2 = wrapped.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "q"}],
        )
        self.assertEqual(r2.choices[0].message.content, "response 1")


# ---------------------------------------------------------------------------
# ResponseCache.wrap() dispatch tests
# ---------------------------------------------------------------------------

class TestWrapDispatch(unittest.TestCase):
    def _cache(self):
        return ResponseCache(path=tempfile.mktemp(suffix=".json"))

    def test_wrap_anthropic(self):
        cache = self._cache()
        client = FakeAnthropicClient()
        wrapped = cache.wrap(client)
        self.assertIsInstance(wrapped, CachedAnthropicClient)

    def test_wrap_openai(self):
        cache = self._cache()
        client = FakeOpenAIClient()
        wrapped = cache.wrap(client)
        self.assertIsInstance(wrapped, CachedOpenAIClient)

    def test_wrap_unknown_raises(self):
        cache = self._cache()

        class WeirdClient:
            __module__ = "some_other_sdk"

        with self.assertRaises(ValueError):
            cache.wrap(WeirdClient())


if __name__ == "__main__":
    unittest.main()
