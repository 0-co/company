import asyncio
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_router import Router, Route, RouterResult, NoMatchingRoute
from agent_router.rules import input_tokens_under, always


# ---------------------------------------------------------------------------
# Mock clients
# ---------------------------------------------------------------------------

class MockAnthropicClient:
    """Anthropic-like client: has .messages attribute."""
    def __init__(self):
        self.last_call = {}

    class _Messages:
        def __init__(self, owner):
            self._owner = owner

        def create(self, **kwargs):
            self._owner.last_call = kwargs

            class MockContent:
                text = "test response"

            class MockResponse:
                content = [MockContent()]
                model = kwargs.get('model', 'test-model')

            return MockResponse()

    def __init__(self):
        self.last_call = {}
        self.messages = self._Messages(self)


class MockOpenAIClient:
    """OpenAI-like client: has .chat attribute."""
    def __init__(self):
        self.last_call = {}

    class _Completions:
        def __init__(self, owner):
            self._owner = owner

        def create(self, **kwargs):
            self._owner.last_call = kwargs

            class MockMessage:
                content = "test response"

            class MockChoice:
                message = MockMessage()

            class MockResponse:
                choices = [MockChoice()]
                model = kwargs.get('model', 'test-model')

            return MockResponse()

    class _Chat:
        def __init__(self, owner):
            self._owner = owner
            self.completions = None  # will be set below

    def __init__(self):
        self.last_call = {}
        chat = self._Chat(self)
        chat.completions = self._Completions(self)
        self.chat = chat


class MockAsyncAnthropicClient:
    """Async Anthropic-like client."""
    def __init__(self):
        self.last_call = {}

    class _AsyncMessages:
        def __init__(self, owner):
            self._owner = owner

        async def create(self, **kwargs):
            self._owner.last_call = kwargs

            class MockContent:
                text = "async test response"

            class MockResponse:
                content = [MockContent()]
                model = kwargs.get('model', 'test-model')

            return MockResponse()

    def __init__(self):
        self.last_call = {}
        self.messages = self._AsyncMessages(self)


# ---------------------------------------------------------------------------
# Tests: Route.matches()
# ---------------------------------------------------------------------------

class TestRouteMatches(unittest.TestCase):
    def test_matches_returns_true_when_all_conditions_pass(self):
        route = Route("model-a", conditions=[
            lambda msgs, **ctx: True,
            lambda msgs, **ctx: True,
        ])
        self.assertTrue(route.matches([{"role": "user", "content": "hello"}]))

    def test_matches_returns_false_when_any_condition_fails(self):
        route = Route("model-a", conditions=[
            lambda msgs, **ctx: True,
            lambda msgs, **ctx: False,
        ])
        self.assertFalse(route.matches([{"role": "user", "content": "hello"}]))

    def test_matches_with_empty_conditions_always_true(self):
        route = Route("default-model")
        self.assertTrue(route.matches([]))
        self.assertTrue(route.matches([{"role": "user", "content": "x" * 10000}]))

    def test_matches_passes_context_to_conditions(self):
        received = {}

        def cond(messages, **ctx):
            received.update(ctx)
            return True

        route = Route("model-a", conditions=[cond])
        route.matches([], foo="bar", baz=42)
        self.assertEqual(received, {"foo": "bar", "baz": 42})

    def test_matches_all_conditions_receive_messages(self):
        received_msgs = []

        def cond(messages, **ctx):
            received_msgs.append(messages)
            return True

        msgs = [{"role": "user", "content": "hi"}]
        route = Route("model-a", conditions=[cond])
        route.matches(msgs)
        self.assertEqual(received_msgs[0], msgs)


# ---------------------------------------------------------------------------
# Tests: Router.select_route()
# ---------------------------------------------------------------------------

class TestRouterSelectRoute(unittest.TestCase):
    def test_returns_first_matching_route(self):
        route_a = Route("model-a", conditions=[lambda msgs, **ctx: True])
        route_b = Route("model-b", conditions=[lambda msgs, **ctx: True])
        router = Router([route_a, route_b])
        selected = router.select_route([])
        self.assertIs(selected, route_a)

    def test_skips_non_matching_routes(self):
        route_a = Route("model-a", conditions=[lambda msgs, **ctx: False])
        route_b = Route("model-b", conditions=[lambda msgs, **ctx: True])
        router = Router([route_a, route_b])
        selected = router.select_route([])
        self.assertIs(selected, route_b)

    def test_raises_no_matching_route_if_nothing_matches(self):
        route_a = Route("model-a", conditions=[lambda msgs, **ctx: False])
        router = Router([route_a])
        with self.assertRaises(NoMatchingRoute):
            router.select_route([])

    def test_single_route_no_conditions_always_selected(self):
        route = Route("only-model")
        router = Router([route])
        selected = router.select_route([])
        self.assertIs(selected, route)


# ---------------------------------------------------------------------------
# Tests: Router.complete() with Anthropic client
# ---------------------------------------------------------------------------

class TestRouterCompleteAnthropic(unittest.TestCase):
    def setUp(self):
        self.client = MockAnthropicClient()

    def test_calls_correct_model(self):
        route = Route("claude-haiku-4-5-20251001", max_tokens=512, name="quick")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        result = router.complete(self.client, messages)
        self.assertEqual(result.model, "claude-haiku-4-5-20251001")

    def test_passes_system_to_anthropic_client(self):
        route = Route("claude-haiku-4-5-20251001")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        router.complete(self.client, messages, system="You are helpful.")
        self.assertEqual(self.client.last_call.get("system"), "You are helpful.")

    def test_passes_max_tokens_from_route(self):
        route = Route("claude-haiku-4-5-20251001", max_tokens=256)
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        router.complete(self.client, messages)
        self.assertEqual(self.client.last_call.get("max_tokens"), 256)

    def test_passes_extra_params(self):
        route = Route("claude-haiku-4-5-20251001")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        router.complete(self.client, messages, extra_params={"temperature": 0.5})
        self.assertEqual(self.client.last_call.get("temperature"), 0.5)

    def test_returns_router_result(self):
        route = Route("claude-haiku-4-5-20251001")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        result = router.complete(self.client, messages)
        self.assertIsInstance(result, RouterResult)

    def test_complete_without_system_no_system_key(self):
        route = Route("claude-haiku-4-5-20251001")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        router.complete(self.client, messages)
        self.assertNotIn("system", self.client.last_call)

    def test_extra_params_does_not_mutate_original(self):
        route = Route("model-a")
        router = Router([route])
        messages = [{"role": "user", "content": "hi"}]
        original = {"temperature": 0.7}
        router.complete(self.client, messages, extra_params=original)
        self.assertNotIn("model", original)


# ---------------------------------------------------------------------------
# Tests: Router.complete() with OpenAI client
# ---------------------------------------------------------------------------

class TestRouterCompleteOpenAI(unittest.TestCase):
    def setUp(self):
        self.client = MockOpenAIClient()

    def test_calls_correct_model(self):
        route = Route("gpt-4o-mini", max_tokens=512, name="cheap")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        result = router.complete(self.client, messages)
        self.assertEqual(result.model, "gpt-4o-mini")

    def test_passes_system_as_message(self):
        route = Route("gpt-4o-mini")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        router.complete(self.client, messages, system="Be concise.")
        sent_messages = self.client.last_call.get("messages", [])
        self.assertEqual(sent_messages[0]["role"], "system")
        self.assertEqual(sent_messages[0]["content"], "Be concise.")

    def test_passes_max_tokens_from_route(self):
        route = Route("gpt-4o-mini", max_tokens=128)
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        router.complete(self.client, messages)
        self.assertEqual(self.client.last_call.get("max_tokens"), 128)

    def test_passes_extra_params(self):
        route = Route("gpt-4o-mini")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        router.complete(self.client, messages, extra_params={"temperature": 0.3})
        self.assertEqual(self.client.last_call.get("temperature"), 0.3)

    def test_returns_router_result(self):
        route = Route("gpt-4o-mini")
        router = Router([route])
        messages = [{"role": "user", "content": "hello"}]
        result = router.complete(self.client, messages)
        self.assertIsInstance(result, RouterResult)


# ---------------------------------------------------------------------------
# Tests: RouterResult
# ---------------------------------------------------------------------------

class TestRouterResult(unittest.TestCase):
    def _make_anthropic_response(self):
        class MockContent:
            text = "anthropic text"

        class MockResponse:
            content = [MockContent()]
            model = "claude-haiku-4-5-20251001"

        return MockResponse()

    def _make_openai_response(self):
        class MockMessage:
            content = "openai text"

        class MockChoice:
            message = MockMessage()

        class MockResponse:
            choices = [MockChoice()]
            model = "gpt-4o-mini"

        return MockResponse()

    def test_route_name_returns_name_when_set(self):
        route = Route("model-x", name="fast")
        result = RouterResult(route=route, response=None, model="model-x")
        self.assertEqual(result.route_name, "fast")

    def test_route_name_returns_model_when_name_not_set(self):
        route = Route("claude-sonnet-4-6")
        result = RouterResult(route=route, response=None, model="claude-sonnet-4-6")
        self.assertEqual(result.route_name, "claude-sonnet-4-6")

    def test_route_name_returns_model_when_name_is_empty_string(self):
        route = Route("model-z", name="")
        result = RouterResult(route=route, response=None, model="model-z")
        self.assertEqual(result.route_name, "model-z")

    def test_text_extracts_from_anthropic_response(self):
        route = Route("model-a")
        result = RouterResult(route=route, response=self._make_anthropic_response(), model="model-a")
        self.assertEqual(result.text(), "anthropic text")

    def test_text_extracts_from_openai_response(self):
        route = Route("model-a")
        result = RouterResult(route=route, response=self._make_openai_response(), model="model-a")
        self.assertEqual(result.text(), "openai text")


# ---------------------------------------------------------------------------
# Tests: async acomplete()
# ---------------------------------------------------------------------------

class TestRouterAcomplete(unittest.TestCase):
    def test_acomplete_works_with_mock_async_client(self):
        client = MockAsyncAnthropicClient()
        route = Route("claude-haiku-4-5-20251001", max_tokens=256, name="async-test")
        router = Router([route])
        messages = [{"role": "user", "content": "hello async"}]

        result = asyncio.get_event_loop().run_until_complete(
            router.acomplete(client, messages, system="Be helpful.")
        )
        self.assertIsInstance(result, RouterResult)
        self.assertEqual(result.model, "claude-haiku-4-5-20251001")
        self.assertEqual(result.route_name, "async-test")
        self.assertEqual(result.text(), "async test response")

    def test_acomplete_passes_system(self):
        client = MockAsyncAnthropicClient()
        route = Route("model-a")
        router = Router([route])
        messages = [{"role": "user", "content": "hi"}]

        asyncio.get_event_loop().run_until_complete(
            router.acomplete(client, messages, system="sys prompt")
        )
        self.assertEqual(client.last_call.get("system"), "sys prompt")


# ---------------------------------------------------------------------------
# Tests: Router with single route
# ---------------------------------------------------------------------------

class TestRouterSingleRoute(unittest.TestCase):
    def test_single_route_always_used(self):
        client = MockAnthropicClient()
        route = Route("only-model", max_tokens=100)
        router = Router([route])
        messages = [{"role": "user", "content": "test"}]
        result = router.complete(client, messages)
        self.assertEqual(result.model, "only-model")

    def test_router_selects_route_by_condition(self):
        client = MockAnthropicClient()
        cheap = Route(
            "cheap-model",
            conditions=[input_tokens_under(50)],
            max_tokens=256,
            name="cheap",
        )
        default = Route("expensive-model", max_tokens=2048, name="default")
        router = Router([cheap, default])

        short_messages = [{"role": "user", "content": "hi"}]
        result = router.complete(client, short_messages)
        self.assertEqual(result.model, "cheap-model")
        self.assertEqual(result.route_name, "cheap")

        long_messages = [{"role": "user", "content": "x" * 1000}]
        result = router.complete(client, long_messages)
        self.assertEqual(result.model, "expensive-model")
        self.assertEqual(result.route_name, "default")


if __name__ == "__main__":
    unittest.main()
