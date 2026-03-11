"""Tests for RetrySchema (uses mock clients — no real API calls)."""

import asyncio
import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch, call

from agent_schema import RetrySchema, SchemaValidationError, SchemaMaxRetriesExceeded


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def _anthropic_response(text: str) -> MagicMock:
    """Build a fake Anthropic response object."""
    block = MagicMock()
    block.text = text
    response = MagicMock()
    response.content = [block]
    return response


def _openai_response(text: str) -> MagicMock:
    """Build a fake OpenAI response object."""
    choice = MagicMock()
    choice.message.content = text
    response = MagicMock()
    response.choices = [choice]
    return response


def _make_anthropic_client(*responses):
    """Client with .messages.create returning responses in order."""
    client = MagicMock(spec=["messages"])
    client.messages = MagicMock()
    client.messages.create = MagicMock(side_effect=list(responses))
    return client


def _make_openai_client(*responses):
    """Client with .chat.completions.create returning responses in order."""
    client = MagicMock(spec=["chat"])
    client.chat = MagicMock()
    client.chat.completions = MagicMock()
    client.chat.completions.create = MagicMock(side_effect=list(responses))
    return client


SCHEMA = {
    "type": "object",
    "required": ["name", "score"],
    "properties": {
        "name": {"type": "string"},
        "score": {"type": "number"},
    },
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRetrySchemaSync(unittest.TestCase):

    # ------------------------------------------------------------------
    # Client detection
    # ------------------------------------------------------------------

    def test_anthropic_client_detected(self):
        client = MagicMock(spec=["messages"])
        rs = RetrySchema(client, model="claude-3-5-haiku-latest")
        self.assertTrue(rs._is_anthropic())
        self.assertFalse(rs._is_openai())

    def test_openai_client_detected(self):
        client = MagicMock(spec=["chat"])
        rs = RetrySchema(client, model="gpt-4o-mini")
        self.assertTrue(rs._is_openai())
        self.assertFalse(rs._is_anthropic())

    # ------------------------------------------------------------------
    # Successful on first try
    # ------------------------------------------------------------------

    def test_anthropic_success_first_try(self):
        valid_json = json.dumps({"name": "Alice", "score": 99})
        client = _make_anthropic_client(_anthropic_response(valid_json))
        rs = RetrySchema(client, model="claude-test", max_retries=3)
        result = rs.complete([{"role": "user", "content": "give me json"}], SCHEMA)
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(result["score"], 99)
        self.assertEqual(client.messages.create.call_count, 1)

    def test_openai_success_first_try(self):
        valid_json = json.dumps({"name": "Bob", "score": 50})
        client = _make_openai_client(_openai_response(valid_json))
        rs = RetrySchema(client, model="gpt-test", max_retries=3)
        result = rs.complete([{"role": "user", "content": "go"}], SCHEMA)
        self.assertEqual(result["name"], "Bob")

    def test_success_with_markdown_wrapped_json(self):
        """LLM wraps JSON in ```json ... ``` — should still succeed."""
        text = "```json\n{\"name\": \"Carol\", \"score\": 77}\n```"
        client = _make_anthropic_client(_anthropic_response(text))
        rs = RetrySchema(client, model="x", max_retries=3)
        result = rs.complete([{"role": "user", "content": "hi"}], SCHEMA)
        self.assertEqual(result["name"], "Carol")

    # ------------------------------------------------------------------
    # Retry on validation failure
    # ------------------------------------------------------------------

    def test_retry_on_schema_failure_succeeds_second_try(self):
        bad = json.dumps({"name": "Alice"})           # missing score
        good = json.dumps({"name": "Alice", "score": 10})
        client = _make_anthropic_client(
            _anthropic_response(bad),
            _anthropic_response(good),
        )
        rs = RetrySchema(client, model="x", max_retries=3)
        result = rs.complete([{"role": "user", "content": "hi"}], SCHEMA)
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(client.messages.create.call_count, 2)

    def test_retry_message_contains_validation_errors(self):
        """Second call's messages should include the error from the first response."""
        bad = json.dumps({"name": "Alice"})   # missing score
        good = json.dumps({"name": "Alice", "score": 20})
        client = _make_anthropic_client(
            _anthropic_response(bad),
            _anthropic_response(good),
        )
        rs = RetrySchema(client, model="x", max_retries=3)
        rs.complete([{"role": "user", "content": "hi"}], SCHEMA)

        second_call_kwargs = client.messages.create.call_args_list[1]
        messages_sent = second_call_kwargs[1]["messages"]

        # The last two messages should be assistant (bad) + user (error)
        last_user_msg = messages_sent[-1]
        self.assertEqual(last_user_msg["role"], "user")
        self.assertIn("validation errors", last_user_msg["content"].lower())
        self.assertIn("score", last_user_msg["content"])

    def test_retry_on_invalid_json_followed_by_valid(self):
        """First response is not JSON at all — should retry."""
        client = _make_anthropic_client(
            _anthropic_response("I cannot provide that."),
            _anthropic_response(json.dumps({"name": "X", "score": 1})),
        )
        rs = RetrySchema(client, model="x", max_retries=3)
        result = rs.complete([{"role": "user", "content": "q"}], SCHEMA)
        self.assertEqual(result["name"], "X")

    # ------------------------------------------------------------------
    # Max retries exceeded
    # ------------------------------------------------------------------

    def test_max_retries_exceeded_raises(self):
        bad = json.dumps({"name": "only"})  # missing score every time
        client = _make_anthropic_client(
            _anthropic_response(bad),
            _anthropic_response(bad),
            _anthropic_response(bad),
        )
        rs = RetrySchema(client, model="x", max_retries=3)
        with self.assertRaises(SchemaMaxRetriesExceeded) as ctx:
            rs.complete([{"role": "user", "content": "q"}], SCHEMA)
        self.assertEqual(ctx.exception.attempts, 3)
        self.assertTrue(len(ctx.exception.last_errors) > 0)

    def test_max_retries_call_count(self):
        """Exactly max_retries calls should be made before raising."""
        bad = json.dumps({"name": "only"})
        client = _make_anthropic_client(
            _anthropic_response(bad),
            _anthropic_response(bad),
            _anthropic_response(bad),
            _anthropic_response(bad),  # extra — should NOT be called
        )
        rs = RetrySchema(client, model="x", max_retries=3)
        with self.assertRaises(SchemaMaxRetriesExceeded):
            rs.complete([{"role": "user", "content": "q"}], SCHEMA)
        self.assertEqual(client.messages.create.call_count, 3)

    def test_max_retries_1_exhausted_immediately(self):
        bad = json.dumps({"wrong": "fields"})
        client = _make_anthropic_client(_anthropic_response(bad))
        rs = RetrySchema(client, model="x", max_retries=1)
        with self.assertRaises(SchemaMaxRetriesExceeded) as ctx:
            rs.complete([{"role": "user", "content": "q"}], SCHEMA)
        self.assertEqual(ctx.exception.attempts, 1)

    # ------------------------------------------------------------------
    # system parameter
    # ------------------------------------------------------------------

    def test_system_param_passed_to_anthropic(self):
        valid_json = json.dumps({"name": "A", "score": 1})
        client = _make_anthropic_client(_anthropic_response(valid_json))
        rs = RetrySchema(client, model="x")
        rs.complete(
            [{"role": "user", "content": "hi"}],
            SCHEMA,
            system="You are helpful.",
        )
        call_kwargs = client.messages.create.call_args[1]
        self.assertEqual(call_kwargs["system"], "You are helpful.")

    def test_system_param_prepended_to_openai_messages(self):
        valid_json = json.dumps({"name": "A", "score": 1})
        client = _make_openai_client(_openai_response(valid_json))
        rs = RetrySchema(client, model="x")
        rs.complete(
            [{"role": "user", "content": "hi"}],
            SCHEMA,
            system="You are helpful.",
        )
        call_kwargs = client.chat.completions.create.call_args[1]
        first_msg = call_kwargs["messages"][0]
        self.assertEqual(first_msg["role"], "system")
        self.assertEqual(first_msg["content"], "You are helpful.")

    # ------------------------------------------------------------------
    # Caller messages not mutated
    # ------------------------------------------------------------------

    def test_original_messages_not_mutated(self):
        """RetrySchema should not modify the caller's message list."""
        bad = json.dumps({"name": "only"})
        good = json.dumps({"name": "Y", "score": 5})
        client = _make_anthropic_client(
            _anthropic_response(bad),
            _anthropic_response(good),
        )
        rs = RetrySchema(client, model="x", max_retries=3)
        original = [{"role": "user", "content": "hi"}]
        original_copy = [dict(m) for m in original]
        rs.complete(original, SCHEMA)
        self.assertEqual(original, original_copy)


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestRetrySchemaAsync(unittest.TestCase):

    def _run(self, coro):
        return asyncio.get_event_loop().run_until_complete(coro)

    def _make_async_anthropic_client(self, *texts):
        client = MagicMock(spec=["messages"])
        client.messages = MagicMock()
        responses = [_anthropic_response(t) for t in texts]
        client.messages.create = AsyncMock(side_effect=responses)
        return client

    def _make_async_openai_client(self, *texts):
        client = MagicMock(spec=["chat"])
        client.chat = MagicMock()
        client.chat.completions = MagicMock()
        responses = [_openai_response(t) for t in texts]
        client.chat.completions.create = AsyncMock(side_effect=responses)
        return client

    def test_async_anthropic_success_first_try(self):
        valid = json.dumps({"name": "Async", "score": 7})
        client = self._make_async_anthropic_client(valid)
        rs = RetrySchema(client, model="x", max_retries=3)
        result = self._run(rs.acomplete([{"role": "user", "content": "q"}], SCHEMA))
        self.assertEqual(result["name"], "Async")

    def test_async_openai_success_first_try(self):
        valid = json.dumps({"name": "AsyncOAI", "score": 3})
        client = self._make_async_openai_client(valid)
        rs = RetrySchema(client, model="x", max_retries=3)
        result = self._run(rs.acomplete([{"role": "user", "content": "q"}], SCHEMA))
        self.assertEqual(result["name"], "AsyncOAI")

    def test_async_retry_then_succeed(self):
        bad = json.dumps({"name": "only"})
        good = json.dumps({"name": "Fixed", "score": 99})
        client = self._make_async_anthropic_client(bad, good)
        rs = RetrySchema(client, model="x", max_retries=3)
        result = self._run(rs.acomplete([{"role": "user", "content": "q"}], SCHEMA))
        self.assertEqual(result["name"], "Fixed")
        self.assertEqual(client.messages.create.call_count, 2)

    def test_async_max_retries_exceeded(self):
        bad = json.dumps({"name": "only"})
        client = self._make_async_anthropic_client(bad, bad, bad)
        rs = RetrySchema(client, model="x", max_retries=3)
        with self.assertRaises(SchemaMaxRetriesExceeded):
            self._run(rs.acomplete([{"role": "user", "content": "q"}], SCHEMA))


if __name__ == "__main__":
    unittest.main()
