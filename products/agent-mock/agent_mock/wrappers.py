"""agent-mock — client wrappers."""

from typing import Any


class _MockedMessages:
    def __init__(self, real_messages: Any, session: Any) -> None:
        self._real = real_messages
        self._session = session

    def create(self, model: str, messages: Any, **kwargs: Any) -> Any:
        return self._session._handle(
            model=model,
            messages=messages,
            real_client_fn=lambda: self._real.create(model=model, messages=messages, **kwargs),
            **kwargs,
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)


class MockedAnthropicClient:
    """Anthropic client with mocked messages.create()."""

    def __init__(self, real_client: Any, session: Any) -> None:
        self._real = real_client
        self._session = session
        self.messages = _MockedMessages(real_client.messages, session)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)

    def __repr__(self) -> str:
        return f"MockedAnthropicClient(session={self._session!r})"


class _MockedCompletions:
    def __init__(self, real_completions: Any, session: Any) -> None:
        self._real = real_completions
        self._session = session

    def create(self, model: str, messages: Any, **kwargs: Any) -> Any:
        if kwargs.get("stream"):
            return self._real.create(model=model, messages=messages, **kwargs)
        return self._session._handle(
            model=model,
            messages=messages,
            real_client_fn=lambda: self._real.create(model=model, messages=messages, **kwargs),
            **kwargs,
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)


class _MockedChat:
    def __init__(self, real_chat: Any, session: Any) -> None:
        self._real = real_chat
        self.completions = _MockedCompletions(real_chat.completions, session)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)


class MockedOpenAIClient:
    """OpenAI client with mocked chat.completions.create()."""

    def __init__(self, real_client: Any, session: Any) -> None:
        self._real = real_client
        self._session = session
        self.chat = _MockedChat(real_client.chat, session)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)

    def __repr__(self) -> str:
        return f"MockedOpenAIClient(session={self._session!r})"
