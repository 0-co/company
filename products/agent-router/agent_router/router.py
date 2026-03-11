from dataclasses import dataclass, field
from typing import Callable, Optional, Any


@dataclass
class Route:
    """
    A model + conditions for when to use it.

    Routes are evaluated in order. First matching route wins.
    The last route in the list acts as the default (no conditions = always matches).
    """
    model: str                          # e.g. "claude-haiku-4-5-20251001"
    conditions: list = field(default_factory=list)  # all must pass
    max_tokens: int = 1024              # max_tokens for this route's responses
    name: str = ""                      # optional label for logging/debugging

    def matches(self, messages: list, **context) -> bool:
        """Returns True if all conditions pass for this route."""
        return all(cond(messages, **context) for cond in self.conditions)


class NoMatchingRoute(Exception):
    """Raised when no route matches and there's no default route."""
    pass


class Router:
    """
    Routes LLM API calls to different models based on rules.

    Usage:
        router = Router([
            # Short inputs -> cheap model
            Route("claude-haiku-4-5-20251001",
                  conditions=[input_tokens_under(500)],
                  max_tokens=512,
                  name="quick"),
            # Default -> full model
            Route("claude-sonnet-4-6",
                  max_tokens=2048,
                  name="full"),
        ])

        result = router.complete(client, messages, system="You are helpful.")
        # Returns: RouterResult with model used, response, route_name
    """

    def __init__(self, routes: list):
        self.routes = routes

    def select_route(self, messages: list, **context) -> Route:
        """
        Select first matching route.

        Raises NoMatchingRoute if no route matches (shouldn't happen if last route has no conditions).
        """
        for route in self.routes:
            if route.matches(messages, **context):
                return route
        raise NoMatchingRoute(
            "No route matched the given messages. "
            "Add a default route with no conditions as the last route."
        )

    def complete(
        self,
        client,
        messages: list,
        system: str = None,
        extra_params: dict = None,
        **context
    ) -> "RouterResult":
        """
        Route and complete. Returns RouterResult.

        Detects Anthropic vs OpenAI client by hasattr(client, 'messages') vs hasattr(client, 'chat').
        """
        route = self.select_route(messages, **context)
        params = extra_params.copy() if extra_params else {}
        params["model"] = route.model
        params["max_tokens"] = route.max_tokens
        params["messages"] = messages

        if hasattr(client, "messages"):
            # Anthropic-style client
            if system is not None:
                params["system"] = system
            response = client.messages.create(**params)
        elif hasattr(client, "chat"):
            # OpenAI-style client
            if system is not None:
                messages_with_system = [{"role": "system", "content": system}] + list(messages)
                params["messages"] = messages_with_system
            response = client.chat.completions.create(**params)
        else:
            raise ValueError(
                "Unrecognized client type. Expected Anthropic client (has .messages) "
                "or OpenAI client (has .chat)."
            )

        return RouterResult(route=route, response=response, model=route.model)

    async def acomplete(
        self,
        client,
        messages: list,
        system: str = None,
        extra_params: dict = None,
        **context
    ) -> "RouterResult":
        """Async version."""
        route = self.select_route(messages, **context)
        params = extra_params.copy() if extra_params else {}
        params["model"] = route.model
        params["max_tokens"] = route.max_tokens
        params["messages"] = messages

        if hasattr(client, "messages"):
            # Anthropic-style async client
            if system is not None:
                params["system"] = system
            response = await client.messages.create(**params)
        elif hasattr(client, "chat"):
            # OpenAI-style async client
            if system is not None:
                messages_with_system = [{"role": "system", "content": system}] + list(messages)
                params["messages"] = messages_with_system
            response = await client.chat.completions.create(**params)
        else:
            raise ValueError(
                "Unrecognized client type. Expected Anthropic client (has .messages) "
                "or OpenAI client (has .chat)."
            )

        return RouterResult(route=route, response=response, model=route.model)


@dataclass
class RouterResult:
    """Result of a Router.complete() call."""
    route: Route               # which route was used
    response: Any              # raw response from the client
    model: str                 # model that was called

    @property
    def route_name(self) -> str:
        return self.route.name or self.route.model

    def text(self) -> str:
        """Extract text from response regardless of client type (Anthropic or OpenAI)."""
        # Anthropic response: response.content[0].text
        if hasattr(self.response, "content") and isinstance(self.response.content, list):
            if self.response.content and hasattr(self.response.content[0], "text"):
                return self.response.content[0].text

        # OpenAI response: response.choices[0].message.content
        if hasattr(self.response, "choices") and isinstance(self.response.choices, list):
            if self.response.choices and hasattr(self.response.choices[0], "message"):
                return self.response.choices[0].message.content

        raise ValueError(
            "Cannot extract text from response. "
            "Expected Anthropic (response.content[0].text) or OpenAI (response.choices[0].message.content) format."
        )
