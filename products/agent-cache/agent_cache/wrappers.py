"""agent-cache — thin wrappers around Anthropic and OpenAI clients."""

from typing import Any


class _CachedMessages:
    """Wraps anthropic.resources.Messages to intercept .create() calls."""

    def __init__(self, real_messages: Any, cache: Any) -> None:
        self._real = real_messages
        self._cache = cache

    def create(self, model: str, messages: Any, **kwargs: Any) -> Any:
        key = self._cache.make_key(model, messages, **kwargs)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        response = self._real.create(model=model, messages=messages, **kwargs)
        self._cache.set(key, response, model=model)
        return response

    # Pass through everything else (stream, batch, etc.)
    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)


class CachedAnthropicClient:
    """
    Wraps an anthropic.Anthropic (or AsyncAnthropic) client.
    .messages.create() calls are transparently cached.

    All other attributes pass through to the real client.
    """

    def __init__(self, real_client: Any, cache: Any) -> None:
        self._real = real_client
        self._cache = cache
        self.messages = _CachedMessages(real_client.messages, cache)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)

    def __repr__(self) -> str:
        return f"CachedAnthropicClient(cache={self._cache!r})"


class _CachedCompletions:
    """Wraps openai.resources.chat.Completions to intercept .create() calls."""

    def __init__(self, real_completions: Any, cache: Any) -> None:
        self._real = real_completions
        self._cache = cache

    def create(self, model: str, messages: Any, **kwargs: Any) -> Any:
        # Don't cache streaming responses
        if kwargs.get("stream"):
            return self._real.create(model=model, messages=messages, **kwargs)

        key = self._cache.make_key(model, messages, **kwargs)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        response = self._real.create(model=model, messages=messages, **kwargs)
        self._cache.set(key, response, model=model)
        return response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)


class _CachedChat:
    def __init__(self, real_chat: Any, cache: Any) -> None:
        self._real = real_chat
        self.completions = _CachedCompletions(real_chat.completions, cache)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)


class CachedOpenAIClient:
    """
    Wraps an openai.OpenAI (or AsyncOpenAI) client.
    .chat.completions.create() calls are transparently cached.

    All other attributes pass through to the real client.
    """

    def __init__(self, real_client: Any, cache: Any) -> None:
        self._real = real_client
        self._cache = cache
        self.chat = _CachedChat(real_client.chat, cache)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)

    def __repr__(self) -> str:
        return f"CachedOpenAIClient(cache={self._cache!r})"
