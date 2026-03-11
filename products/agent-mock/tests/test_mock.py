"""Tests for agent-mock."""

import json
import os
import sys
import tempfile
import unittest
import types

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_mock import MockSession, MockError
from agent_mock.mock import _make_key, _fill_defaults, _Cassette


# ---------------------------------------------------------------------------
# Fake SDK clients
# ---------------------------------------------------------------------------

class FakeMessages:
    def __init__(self):
        self.call_count = 0

    def create(self, model, messages, **kwargs):
        self.call_count += 1
        return {
            "id": f"real_msg_{self.call_count}",
            "type": "message",
            "role": "assistant",
            "model": model,
            "content": [{"type": "text", "text": f"real response {self.call_count}"}],
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 10, "output_tokens": 5},
        }


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
        return {
            "id": f"chatcmpl_{self.call_count}",
            "object": "chat.completion",
            "model": model,
            "choices": [{"message": {"role": "assistant", "content": f"real {self.call_count}"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
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
# Core fixture tests
# ---------------------------------------------------------------------------

class TestFixtureMode(unittest.TestCase):
    def _session(self, **kwargs) -> MockSession:
        return MockSession(**kwargs)

    def test_fixture_returns_response(self):
        session = self._session()
        session.on(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hello"}],
            returns={"type": "message", "content": [{"type": "text", "text": "Hi!"}]},
        )
        client = session.wrap(FakeAnthropicClient())
        response = client.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hello"}],
        )
        self.assertEqual(response.content[0].text, "Hi!")

    def test_fixture_not_matched_passes_through(self):
        session = self._session()
        session.on(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hello"}],
            returns={"type": "message", "content": [{"type": "text", "text": "mocked"}]},
        )
        real = FakeAnthropicClient()
        client = session.wrap(real)
        # Different message — should pass through to real client
        response = client.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "different"}],
        )
        self.assertEqual(real.messages.call_count, 1)

    def test_strict_mode_raises_on_unmatched(self):
        session = self._session(strict=True)
        client = session.wrap(FakeAnthropicClient())
        with self.assertRaises(MockError) as ctx:
            client.messages.create(
                model="claude-sonnet-4-6",
                messages=[{"role": "user", "content": "no fixture for this"}],
            )
        self.assertIn("Unexpected call", str(ctx.exception))

    def test_fixture_raises_error(self):
        session = self._session()
        session.on(
            model="m",
            messages=[],
            raises=MockError("Rate limited", status_code=429),
        )
        client = session.wrap(FakeAnthropicClient())
        with self.assertRaises(MockError) as ctx:
            client.messages.create(model="m", messages=[])
        self.assertEqual(ctx.exception.status_code, 429)

    def test_multiple_fixtures(self):
        session = self._session()
        session.on(
            model="m", messages=[{"role": "user", "content": "q1"}],
            returns={"type": "message", "content": [{"type": "text", "text": "a1"}]},
        )
        session.on(
            model="m", messages=[{"role": "user", "content": "q2"}],
            returns={"type": "message", "content": [{"type": "text", "text": "a2"}]},
        )
        client = session.wrap(FakeAnthropicClient())
        r1 = client.messages.create(model="m", messages=[{"role": "user", "content": "q1"}])
        r2 = client.messages.create(model="m", messages=[{"role": "user", "content": "q2"}])
        self.assertEqual(r1.content[0].text, "a1")
        self.assertEqual(r2.content[0].text, "a2")

    def test_sequential_responses(self):
        """Fixture returns different responses on each call."""
        session = self._session()
        session.on(
            model="m", messages=[],
            returns=[
                {"type": "message", "content": [{"type": "text", "text": "first"}]},
                {"type": "message", "content": [{"type": "text", "text": "second"}]},
            ],
        )
        client = session.wrap(FakeAnthropicClient())
        r1 = client.messages.create(model="m", messages=[])
        r2 = client.messages.create(model="m", messages=[])
        r3 = client.messages.create(model="m", messages=[])  # repeats last
        self.assertEqual(r1.content[0].text, "first")
        self.assertEqual(r2.content[0].text, "second")
        self.assertEqual(r3.content[0].text, "second")

    def test_call_count_increments(self):
        session = self._session()
        client = session.wrap(FakeAnthropicClient())
        for _ in range(3):
            client.messages.create(model="m", messages=[{"role": "user", "content": "x"}])
        self.assertEqual(session.call_count, 3)

    def test_reset_clears_fixtures_and_count(self):
        session = self._session()
        session.on(model="m", messages=[], returns={"content": []})
        session._call_count = 5
        session.reset()
        self.assertEqual(len(session._fixtures), 0)
        self.assertEqual(session.call_count, 0)

    def test_passthrough_attributes(self):
        session = self._session()
        real = FakeAnthropicClient()
        client = session.wrap(real)
        self.assertEqual(client.api_key, "sk-test")

    def test_repr(self):
        session = self._session()
        self.assertIn("MockSession", repr(session))

    def test_context_manager(self):
        with MockSession() as session:
            session.on(model="m", messages=[], returns={"content": []})
            self.assertEqual(len(session._fixtures), 1)


# ---------------------------------------------------------------------------
# OpenAI tests
# ---------------------------------------------------------------------------

class TestOpenAIFixtures(unittest.TestCase):
    def test_fixture_returns_response(self):
        session = MockSession()
        session.on(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "hi"}],
            returns={
                "object": "chat.completion",
                "choices": [{"message": {"role": "assistant", "content": "hello"}}],
            },
        )
        client = session.wrap(FakeOpenAIClient())
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "hi"}],
        )
        self.assertEqual(r.choices[0].message.content, "hello")

    def test_streaming_bypasses_mock(self):
        session = MockSession(strict=True)
        real = FakeOpenAIClient()
        client = session.wrap(real)
        # stream=True bypasses mock — should call real client
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "x"}],
            stream=True,
        )
        self.assertEqual(real.chat.completions.call_count, 1)


# ---------------------------------------------------------------------------
# Cassette tests
# ---------------------------------------------------------------------------

class TestCassette(unittest.TestCase):
    def test_record_and_find(self):
        cassette = _Cassette()
        key = "abc123"
        cassette.record(key, {"model": "m"}, {"content": "resp"})
        result = cassette.find(key)
        self.assertEqual(result, {"content": "resp"})

    def test_find_missing_returns_none(self):
        cassette = _Cassette()
        self.assertIsNone(cassette.find("nonexistent"))

    def test_save_and_load(self):
        cassette = _Cassette()
        cassette.record("key1", {"model": "m"}, {"text": "hello"})
        cassette.record("key2", {"model": "n"}, {"text": "world"})

        tf = tempfile.mktemp(suffix=".json")
        cassette.save(tf)

        loaded = _Cassette.load(tf)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded.find("key1"), {"text": "hello"})
        self.assertEqual(loaded.find("key2"), {"text": "world"})

    def test_len(self):
        cassette = _Cassette()
        self.assertEqual(len(cassette), 0)
        cassette.record("k", {}, {})
        self.assertEqual(len(cassette), 1)


class TestRecordMode(unittest.TestCase):
    def test_record_context_saves_to_file(self):
        real = FakeAnthropicClient()
        tf = tempfile.mktemp(suffix=".json")

        with MockSession.record(tf) as session:
            client = session.wrap(real)
            client.messages.create(
                model="m",
                messages=[{"role": "user", "content": "q"}],
            )

        # Real client was called
        self.assertEqual(real.messages.call_count, 1)

        # Cassette file was created
        self.assertTrue(os.path.exists(tf))
        with open(tf) as f:
            data = json.load(f)
        self.assertEqual(len(data["interactions"]), 1)

    def test_playback_serves_from_cassette(self):
        real = FakeAnthropicClient()
        tf = tempfile.mktemp(suffix=".json")

        # Record
        with MockSession.record(tf) as session:
            client = session.wrap(real)
            client.messages.create(
                model="m",
                messages=[{"role": "user", "content": "q"}],
            )
        first_call_count = real.messages.call_count

        # Playback
        real2 = FakeAnthropicClient()
        with MockSession.playback(tf) as session:
            client2 = session.wrap(real2)
            response = client2.messages.create(
                model="m",
                messages=[{"role": "user", "content": "q"}],
            )

        # Real client NOT called during playback
        self.assertEqual(real2.messages.call_count, 0)
        # Response matches recorded value
        self.assertIn("real response 1", response.content[0].text)

    def test_playback_strict_raises_on_miss(self):
        tf = tempfile.mktemp(suffix=".json")
        # Create empty cassette
        _Cassette().save(tf)

        with MockSession.playback(tf, strict=True) as session:
            client = session.wrap(FakeAnthropicClient())
            with self.assertRaises(MockError) as ctx:
                client.messages.create(model="m", messages=[])
        self.assertIn("cassette_miss", ctx.exception.type)

    def test_playback_non_strict_falls_through(self):
        tf = tempfile.mktemp(suffix=".json")
        _Cassette().save(tf)
        real = FakeAnthropicClient()

        with MockSession.playback(tf, strict=False) as session:
            client = session.wrap(real)
            client.messages.create(model="m", messages=[])

        self.assertEqual(real.messages.call_count, 1)


# ---------------------------------------------------------------------------
# Side effect tests
# ---------------------------------------------------------------------------

class TestSideEffects(unittest.TestCase):
    def test_side_effect_called_with_count(self):
        call_counts = []

        def effect(count):
            call_counts.append(count)
            return types.SimpleNamespace(content=[types.SimpleNamespace(text=f"call {count}")])

        session = MockSession()
        session.on(model="m", messages=[], side_effect=effect)
        client = session.wrap(FakeAnthropicClient())

        r1 = client.messages.create(model="m", messages=[])
        r2 = client.messages.create(model="m", messages=[])

        self.assertEqual(call_counts, [1, 2])
        self.assertEqual(r1.content[0].text, "call 1")
        self.assertEqual(r2.content[0].text, "call 2")


# ---------------------------------------------------------------------------
# _fill_defaults tests
# ---------------------------------------------------------------------------

class TestFillDefaults(unittest.TestCase):
    def test_anthropic_defaults_filled(self):
        partial = {"content": [{"type": "text", "text": "hi"}]}
        filled = _fill_defaults(partial, "claude-sonnet-4-6")
        self.assertEqual(filled["id"], "msg_mock")
        self.assertEqual(filled["type"], "message")
        self.assertEqual(filled["model"], "claude-sonnet-4-6")
        self.assertEqual(filled["content"][0]["text"], "hi")

    def test_openai_defaults_filled(self):
        partial = {"choices": [{"message": {"content": "hi"}}]}
        filled = _fill_defaults(partial, "gpt-4o-mini")
        self.assertEqual(filled["id"], "chatcmpl_mock")
        self.assertEqual(filled["object"], "chat.completion")
        self.assertEqual(filled["model"], "gpt-4o-mini")

    def test_existing_fields_not_overwritten(self):
        partial = {"type": "message", "id": "custom_id", "content": []}
        filled = _fill_defaults(partial, "m")
        self.assertEqual(filled["id"], "custom_id")


# ---------------------------------------------------------------------------
# make_key tests
# ---------------------------------------------------------------------------

class TestMakeKey(unittest.TestCase):
    def test_deterministic(self):
        k1 = _make_key("m", [{"role": "user", "content": "hi"}], temperature=0.5)
        k2 = _make_key("m", [{"role": "user", "content": "hi"}], temperature=0.5)
        self.assertEqual(k1, k2)

    def test_model_differentiates(self):
        k1 = _make_key("model-a", [])
        k2 = _make_key("model-b", [])
        self.assertNotEqual(k1, k2)

    def test_non_match_params_ignored(self):
        k1 = _make_key("m", [], metadata={"user": "alice"})
        k2 = _make_key("m", [], metadata={"user": "bob"})
        self.assertEqual(k1, k2)


if __name__ == "__main__":
    unittest.main()
