"""Tests for agent_fallback.fallback."""

import asyncio
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_fallback.fallback import (
    Fallback,
    FallbackResult,
    Provider,
    ProviderFailed,
)


# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------

class MockContent:
    def __init__(self, text="anthropic response"):
        self.text = text


class MockAnthropicResponse:
    def __init__(self, text="anthropic response", model="claude-test"):
        self.content = [MockContent(text)]
        self.model = model


class MockOpenAIMessage:
    def __init__(self, content="openai response"):
        self.content = content


class MockOpenAIChoice:
    def __init__(self, content="openai response"):
        self.message = MockOpenAIMessage(content)


class MockOpenAIResponse:
    def __init__(self, content="openai response"):
        self.choices = [MockOpenAIChoice(content)]


def _make_status_error(status_code: int) -> Exception:
    """Create a mock exception with a status_code attribute."""
    err = Exception(f"HTTP {status_code}")
    err.status_code = status_code
    return err


class _AnthropicMessages:
    """Inner .messages object for MockAnthropicClient."""

    def __init__(self, client: "MockAnthropicClient"):
        self._client = client

    def create(self, **kwargs):
        self._client.calls.append(kwargs)
        if self._client.network_error:
            raise self._client.network_error
        if self._client.should_fail:
            raise _make_status_error(self._client.status_code or 500)
        return MockAnthropicResponse(model=kwargs.get("model", "claude-test"))


class MockAnthropicClient:
    """Simulates an Anthropic client (has .messages attribute)."""

    def __init__(self, should_fail=False, status_code=None, network_error=None):
        self.should_fail = should_fail
        self.status_code = status_code
        self.network_error = network_error
        self.calls = []
        self._messages = _AnthropicMessages(self)

    @property
    def messages(self):
        return self._messages


class _OpenAICompletions:
    def __init__(self, client: "MockOpenAIClient"):
        self._client = client

    def create(self, **kwargs):
        self._client.calls.append(kwargs)
        if self._client.network_error:
            raise self._client.network_error
        if self._client.should_fail:
            raise _make_status_error(self._client.status_code or 500)
        return MockOpenAIResponse()


class _OpenAIChat:
    def __init__(self, client: "MockOpenAIClient"):
        self.completions = _OpenAICompletions(client)


class MockOpenAIClient:
    """Simulates an OpenAI client (has .chat.completions attribute)."""

    def __init__(self, should_fail=False, status_code=None, network_error=None):
        self.should_fail = should_fail
        self.status_code = status_code
        self.network_error = network_error
        self.calls = []
        self.chat = _OpenAIChat(self)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestFallbackBasic(unittest.TestCase):

    def test_first_provider_succeeds_returns_attempt_1(self):
        client = MockAnthropicClient()
        fb = Fallback([Provider(client, "claude-test", name="anthropic")])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertIsInstance(result, FallbackResult)
        self.assertEqual(result.attempt, 1)
        self.assertEqual(result.provider_name, "anthropic")

    def test_first_provider_fails_retryable_tries_second(self):
        bad_client = MockAnthropicClient(should_fail=True, status_code=500)
        good_client = MockAnthropicClient()
        fb = Fallback([
            Provider(bad_client, "claude-bad", name="bad"),
            Provider(good_client, "claude-good", name="good"),
        ])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.attempt, 2)
        self.assertEqual(result.provider_name, "good")

    def test_both_providers_fail_raises_provider_failed(self):
        bad1 = MockAnthropicClient(should_fail=True, status_code=500)
        bad2 = MockAnthropicClient(should_fail=True, status_code=503)
        fb = Fallback([
            Provider(bad1, "m1", name="p1"),
            Provider(bad2, "m2", name="p2"),
        ])
        with self.assertRaises(ProviderFailed) as ctx:
            fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(len(ctx.exception.errors), 2)

    def test_provider_failed_errors_contains_name_and_exception(self):
        bad = MockAnthropicClient(should_fail=True, status_code=500)
        fb = Fallback([Provider(bad, "m", name="myprovider")])
        with self.assertRaises(ProviderFailed) as ctx:
            fb.complete([{"role": "user", "content": "hi"}])
        name, exc = ctx.exception.errors[0]
        self.assertEqual(name, "myprovider")
        self.assertIsInstance(exc, Exception)

    def test_non_retryable_400_raises_immediately(self):
        bad = MockAnthropicClient(should_fail=True, status_code=400)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1", name="p1"),
            Provider(good, "m2", name="p2"),
        ])
        with self.assertRaises(Exception) as ctx:
            fb.complete([{"role": "user", "content": "hi"}])
        # Should NOT be ProviderFailed
        self.assertNotIsInstance(ctx.exception, ProviderFailed)
        # Second provider was NOT called
        self.assertEqual(len(good.calls), 0)

    def test_non_retryable_401_raises_immediately(self):
        bad = MockAnthropicClient(should_fail=True, status_code=401)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1"),
            Provider(good, "m2"),
        ])
        with self.assertRaises(Exception) as ctx:
            fb.complete([{"role": "user", "content": "hi"}])
        self.assertNotIsInstance(ctx.exception, ProviderFailed)
        self.assertEqual(len(good.calls), 0)

    def test_non_retryable_403_raises_immediately(self):
        bad = MockAnthropicClient(should_fail=True, status_code=403)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1"),
            Provider(good, "m2"),
        ])
        with self.assertRaises(Exception):
            fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(len(good.calls), 0)

    def test_429_not_retryable_does_not_switch_providers(self):
        """429 = rate limit. Provider is up, just throttling. Don't switch."""
        bad = MockAnthropicClient(should_fail=True, status_code=429)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1", name="p1"),
            Provider(good, "m2", name="p2"),
        ])
        with self.assertRaises(Exception) as ctx:
            fb.complete([{"role": "user", "content": "hi"}])
        self.assertNotIsInstance(ctx.exception, ProviderFailed)
        self.assertEqual(len(good.calls), 0)

    def test_http_500_retryable_tries_next(self):
        bad = MockAnthropicClient(should_fail=True, status_code=500)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1"),
            Provider(good, "m2", name="good"),
        ])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.provider_name, "good")

    def test_http_529_retryable_tries_next(self):
        bad = MockAnthropicClient(should_fail=True, status_code=529)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1"),
            Provider(good, "m2", name="g"),
        ])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.provider_name, "g")

    def test_connection_error_retryable(self):
        bad = MockAnthropicClient(network_error=ConnectionError("refused"))
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1", name="bad"),
            Provider(good, "m2", name="good"),
        ])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.provider_name, "good")

    def test_timeout_error_retryable(self):
        bad = MockAnthropicClient(network_error=TimeoutError("timed out"))
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1", name="bad"),
            Provider(good, "m2", name="good"),
        ])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.provider_name, "good")

    def test_os_error_retryable(self):
        bad = MockAnthropicClient(network_error=OSError("network unreachable"))
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1", name="bad"),
            Provider(good, "m2", name="good"),
        ])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.provider_name, "good")

    def test_on_fallback_callback_called_when_falling_back(self):
        called_with = []
        def on_fb(provider, error):
            called_with.append((provider.name, error))

        bad = MockAnthropicClient(should_fail=True, status_code=500)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1", name="first"),
            Provider(good, "m2", name="second"),
        ], on_fallback=on_fb)
        fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(len(called_with), 1)
        self.assertEqual(called_with[0][0], "first")

    def test_on_fallback_not_called_on_success(self):
        called = []
        good = MockAnthropicClient()
        fb = Fallback(
            [Provider(good, "m1", name="p1")],
            on_fallback=lambda p, e: called.append(p),
        )
        fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(called, [])

    def test_fallback_result_text_anthropic_format(self):
        client = MockAnthropicClient()
        fb = Fallback([Provider(client, "claude-test")])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.text(), "anthropic response")

    def test_fallback_result_text_openai_format(self):
        client = MockOpenAIClient()
        fb = Fallback([Provider(client, "gpt-4o")])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.text(), "openai response")

    def test_fallback_result_provider_name_set_correctly(self):
        client = MockAnthropicClient()
        fb = Fallback([Provider(client, "my-model", name="my-provider")])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.provider_name, "my-provider")

    def test_fallback_result_attempt_correct(self):
        bad = MockAnthropicClient(should_fail=True, status_code=503)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1"),
            Provider(good, "m2"),
        ])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.attempt, 2)

    def test_single_provider_success_attempt_is_1(self):
        client = MockAnthropicClient()
        fb = Fallback([Provider(client, "m", name="only")])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.attempt, 1)

    def test_system_prompt_passed_to_anthropic(self):
        client = MockAnthropicClient()
        fb = Fallback([Provider(client, "m")])
        fb.complete([{"role": "user", "content": "hi"}], system="Be helpful.")
        self.assertEqual(client.calls[0]["system"], "Be helpful.")

    def test_system_prompt_passed_to_openai(self):
        client = MockOpenAIClient()
        fb = Fallback([Provider(client, "gpt-4o")])
        fb.complete([{"role": "user", "content": "hi"}], system="Be helpful.")
        messages = client.calls[0]["messages"]
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "Be helpful.")

    def test_extra_params_merged_into_api_call(self):
        client = MockAnthropicClient()
        fb = Fallback([Provider(client, "m")])
        fb.complete(
            [{"role": "user", "content": "hi"}],
            extra_params={"temperature": 0.7},
        )
        self.assertEqual(client.calls[0]["temperature"], 0.7)

    def test_provider_name_defaults_to_model(self):
        client = MockAnthropicClient()
        p = Provider(client, "claude-sonnet-4-6")
        self.assertEqual(p.name, "claude-sonnet-4-6")

    def test_three_provider_chain_third_succeeds(self):
        b1 = MockAnthropicClient(should_fail=True, status_code=500)
        b2 = MockAnthropicClient(should_fail=True, status_code=503)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(b1, "m1", name="p1"),
            Provider(b2, "m2", name="p2"),
            Provider(good, "m3", name="p3"),
        ])
        result = fb.complete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.attempt, 3)
        self.assertEqual(result.provider_name, "p3")

    def test_provider_failed_message_includes_count(self):
        bad = MockAnthropicClient(should_fail=True, status_code=500)
        fb = Fallback([Provider(bad, "m", name="p")])
        with self.assertRaises(ProviderFailed) as ctx:
            fb.complete([{"role": "user", "content": "hi"}])
        self.assertIn("1", str(ctx.exception))

    def test_empty_providers_raises_value_error(self):
        with self.assertRaises(ValueError):
            Fallback([])


class TestFallbackAsync(unittest.IsolatedAsyncioTestCase):

    async def test_async_happy_path(self):
        client = MockAnthropicClient()
        fb = Fallback([Provider(client, "m", name="p")])
        result = await fb.acomplete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.attempt, 1)
        self.assertEqual(result.provider_name, "p")

    async def test_async_fallback_on_retryable_error(self):
        bad = MockAnthropicClient(should_fail=True, status_code=529)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1", name="bad"),
            Provider(good, "m2", name="good"),
        ])
        result = await fb.acomplete([{"role": "user", "content": "hi"}])
        self.assertEqual(result.provider_name, "good")

    async def test_async_non_retryable_raises_immediately(self):
        bad = MockAnthropicClient(should_fail=True, status_code=401)
        good = MockAnthropicClient()
        fb = Fallback([
            Provider(bad, "m1"),
            Provider(good, "m2"),
        ])
        with self.assertRaises(Exception) as ctx:
            await fb.acomplete([{"role": "user", "content": "hi"}])
        self.assertNotIsInstance(ctx.exception, ProviderFailed)

    async def test_async_all_fail_raises_provider_failed(self):
        b1 = MockAnthropicClient(should_fail=True, status_code=500)
        b2 = MockAnthropicClient(should_fail=True, status_code=503)
        fb = Fallback([
            Provider(b1, "m1", name="p1"),
            Provider(b2, "m2", name="p2"),
        ])
        with self.assertRaises(ProviderFailed) as ctx:
            await fb.acomplete([{"role": "user", "content": "hi"}])
        self.assertEqual(len(ctx.exception.errors), 2)

    async def test_async_system_prompt_passed(self):
        client = MockAnthropicClient()
        fb = Fallback([Provider(client, "m")])
        await fb.acomplete([{"role": "user", "content": "hi"}], system="Sys prompt.")
        self.assertEqual(client.calls[0]["system"], "Sys prompt.")


if __name__ == "__main__":
    unittest.main()
