"""Tests for agent-cache."""

import json
import os
import sys
import tempfile
import time
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_cache import ResponseCache, CacheStats
from agent_cache.cache import (
    CacheEntry,
    _dict_to_namespace,
    _serialize_response,
    _extract_token_counts,
    _cost_for,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fake_anthropic_response(model="claude-sonnet-4-6", text="Hello"):
    """Minimal dict mimicking a serialized Anthropic Message."""
    return {
        "id": "msg_test",
        "type": "message",
        "role": "assistant",
        "model": model,
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }


def _fake_openai_response(model="gpt-4o-mini", text="Hi"):
    return {
        "id": "chatcmpl_test",
        "object": "chat.completion",
        "model": model,
        "choices": [{"message": {"role": "assistant", "content": text}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

class TestDictToNamespace(unittest.TestCase):
    def test_simple_dict(self):
        ns = _dict_to_namespace({"a": 1, "b": "x"})
        self.assertEqual(ns.a, 1)
        self.assertEqual(ns.b, "x")

    def test_nested_dict(self):
        ns = _dict_to_namespace({"content": [{"type": "text", "text": "hi"}]})
        self.assertEqual(ns.content[0].type, "text")
        self.assertEqual(ns.content[0].text, "hi")

    def test_passthrough_primitives(self):
        self.assertEqual(_dict_to_namespace(42), 42)
        self.assertEqual(_dict_to_namespace("abc"), "abc")
        self.assertIsNone(_dict_to_namespace(None))

    def test_list_of_dicts(self):
        result = _dict_to_namespace([{"x": 1}, {"x": 2}])
        self.assertEqual(result[0].x, 1)
        self.assertEqual(result[1].x, 2)


class TestExtractTokenCounts(unittest.TestCase):
    def test_anthropic_format(self):
        d = {"usage": {"input_tokens": 100, "output_tokens": 50}}
        self.assertEqual(_extract_token_counts(d), (100, 50))

    def test_openai_format(self):
        d = {"usage": {"prompt_tokens": 80, "completion_tokens": 20, "total_tokens": 100}}
        self.assertEqual(_extract_token_counts(d), (80, 20))

    def test_no_usage(self):
        self.assertEqual(_extract_token_counts({}), (0, 0))

    def test_null_values(self):
        d = {"usage": {"input_tokens": None, "output_tokens": None}}
        self.assertEqual(_extract_token_counts(d), (0, 0))


class TestCostFor(unittest.TestCase):
    def test_known_model(self):
        # claude-sonnet-4-6: $3/M input, $15/M output
        cost = _cost_for("claude-sonnet-4-6", 1_000_000, 0)
        self.assertAlmostEqual(cost, 3.0)
        cost = _cost_for("claude-sonnet-4-6", 0, 1_000_000)
        self.assertAlmostEqual(cost, 15.0)

    def test_unknown_model(self):
        cost = _cost_for("unknown-model-xyz", 1000, 500)
        self.assertEqual(cost, 0.0)


class TestCacheEntry(unittest.TestCase):
    def test_round_trip(self):
        entry = CacheEntry(
            response={"text": "hi"},
            model="claude-sonnet-4-6",
            created_at=1000.0,
            input_tokens=10,
            output_tokens=5,
        )
        entry.hits = 3
        d = entry.to_dict()
        restored = CacheEntry.from_dict(d)
        self.assertEqual(restored.response, {"text": "hi"})
        self.assertEqual(restored.model, "claude-sonnet-4-6")
        self.assertEqual(restored.hits, 3)
        self.assertEqual(restored.input_tokens, 10)


class TestResponseCache(unittest.TestCase):
    def _make_cache(self, **kwargs) -> ResponseCache:
        tf = tempfile.mktemp(suffix=".json")
        return ResponseCache(path=tf, **kwargs)

    def test_miss_returns_none(self):
        cache = self._make_cache()
        self.assertIsNone(cache.get("nonexistent"))

    def test_set_and_get(self):
        cache = self._make_cache()
        resp = _fake_anthropic_response()
        key = cache.make_key("claude-sonnet-4-6", [{"role": "user", "content": "hi"}])
        cache.set(key, resp, model="claude-sonnet-4-6")

        result = cache.get(key)
        self.assertIsNotNone(result)
        self.assertEqual(result.content[0].text, "Hello")

    def test_stats_hit_rate(self):
        cache = self._make_cache()
        resp = _fake_anthropic_response()
        key = cache.make_key("m", [])
        cache.set(key, resp, model="claude-sonnet-4-6")

        cache.get("missing")  # miss
        cache.get(key)        # hit
        cache.get(key)        # hit

        s = cache.stats()
        self.assertEqual(s.hits, 2)
        self.assertEqual(s.misses, 1)
        self.assertAlmostEqual(s.hit_rate, 2/3)

    def test_cost_saved_accumulates(self):
        cache = self._make_cache()
        resp = _fake_anthropic_response(model="claude-sonnet-4-6")
        key = cache.make_key("claude-sonnet-4-6", [])
        cache.set(key, resp, model="claude-sonnet-4-6")
        cache.get(key)

        s = cache.stats()
        self.assertGreater(s.cost_saved_usd, 0)

    def test_ttl_expiry(self):
        cache = self._make_cache(ttl=1)
        resp = _fake_anthropic_response()
        key = cache.make_key("m", [])
        cache.set(key, resp)
        self.assertIsNotNone(cache.get(key))
        time.sleep(1.1)
        self.assertIsNone(cache.get(key))

    def test_clear(self):
        cache = self._make_cache()
        key = cache.make_key("m", [])
        cache.set(key, _fake_anthropic_response())
        self.assertEqual(len(cache), 1)
        cache.clear()
        self.assertEqual(len(cache), 0)

    def test_invalidate(self):
        cache = self._make_cache()
        key = cache.make_key("m", [])
        cache.set(key, _fake_anthropic_response())
        self.assertTrue(cache.invalidate(key))
        self.assertFalse(cache.invalidate(key))
        self.assertEqual(len(cache), 0)

    def test_persistence(self):
        tf = tempfile.mktemp(suffix=".json")
        cache1 = ResponseCache(path=tf)
        key = cache1.make_key("m", [{"role": "user", "content": "q"}])
        cache1.set(key, _fake_anthropic_response(), model="claude-sonnet-4-6")

        cache2 = ResponseCache(path=tf)
        result = cache2.get(key)
        self.assertIsNotNone(result)
        self.assertEqual(result.content[0].text, "Hello")

    def test_max_entries_eviction(self):
        cache = self._make_cache(max_entries=3)
        for i in range(4):
            key = cache.make_key(f"m{i}", [])
            cache.set(key, _fake_anthropic_response(text=str(i)))
        self.assertEqual(len(cache), 3)

    def test_make_key_deterministic(self):
        cache = self._make_cache()
        k1 = cache.make_key("m", [{"role": "user", "content": "hi"}], temperature=0.7)
        k2 = cache.make_key("m", [{"role": "user", "content": "hi"}], temperature=0.7)
        self.assertEqual(k1, k2)

    def test_make_key_differentiates_models(self):
        cache = self._make_cache()
        k1 = cache.make_key("model-a", [])
        k2 = cache.make_key("model-b", [])
        self.assertNotEqual(k1, k2)

    def test_make_key_ignores_non_cacheable_params(self):
        cache = self._make_cache()
        k1 = cache.make_key("m", [], metadata={"user_id": "123"})
        k2 = cache.make_key("m", [], metadata={"user_id": "456"})
        self.assertEqual(k1, k2)

    def test_make_key_respects_cacheable_params(self):
        cache = self._make_cache()
        k1 = cache.make_key("m", [], temperature=0.0)
        k2 = cache.make_key("m", [], temperature=1.0)
        self.assertNotEqual(k1, k2)

    def test_set_accepts_dict_directly(self):
        cache = self._make_cache()
        resp_dict = _fake_anthropic_response()
        key = cache.make_key("m", [])
        cache.set(key, resp_dict, model="claude-sonnet-4-6")
        result = cache.get(key)
        self.assertEqual(result.content[0].text, "Hello")

    def test_corrupt_cache_file_ignored(self):
        tf = tempfile.mktemp(suffix=".json")
        with open(tf, "w") as f:
            f.write("{not valid json")
        cache = ResponseCache(path=tf)
        self.assertEqual(len(cache), 0)

    def test_repr(self):
        cache = self._make_cache()
        r = repr(cache)
        self.assertIn("ResponseCache", r)
        self.assertIn("entries=0", r)

    def test_stats_repr(self):
        s = CacheStats()
        self.assertIn("CacheStats", repr(s))


class TestCacheWithPydanticLike(unittest.TestCase):
    """Test with objects that have model_dump() like real SDK responses."""

    def _fake_pydantic_response(self):
        class FakeUsage:
            input_tokens = 20
            output_tokens = 10
            def model_dump(self):
                return {"input_tokens": 20, "output_tokens": 10}

        class FakeContent:
            type = "text"
            text = "Cached answer"
            def model_dump(self):
                return {"type": "text", "text": "Cached answer"}

        class FakeMessage:
            id = "msg_fake"
            type = "message"
            role = "assistant"
            model = "claude-sonnet-4-6"
            stop_reason = "end_turn"
            def __init__(self):
                self.usage = FakeUsage()
                self.content = [FakeContent()]
            def model_dump(self):
                return {
                    "id": self.id,
                    "type": self.type,
                    "role": self.role,
                    "model": self.model,
                    "content": [c.model_dump() for c in self.content],
                    "stop_reason": self.stop_reason,
                    "usage": self.usage.model_dump(),
                }

        return FakeMessage()

    def test_serialize_pydantic_response(self):
        resp = self._fake_pydantic_response()
        d = _serialize_response(resp)
        self.assertEqual(d["content"][0]["text"], "Cached answer")
        self.assertEqual(d["usage"]["input_tokens"], 20)

    def test_cache_with_pydantic_response(self):
        cache = ResponseCache(path=tempfile.mktemp(suffix=".json"))
        resp = self._fake_pydantic_response()
        key = cache.make_key("claude-sonnet-4-6", [{"role": "user", "content": "q"}])
        cache.set(key, resp, model="claude-sonnet-4-6")

        result = cache.get(key)
        self.assertEqual(result.content[0].text, "Cached answer")
        self.assertEqual(result.usage.input_tokens, 20)


if __name__ == "__main__":
    unittest.main()
