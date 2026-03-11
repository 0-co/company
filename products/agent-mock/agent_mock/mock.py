"""agent-mock — record/replay/fixture LLM responses for testing AI agents."""

import hashlib
import json
import os
import types
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union


class MockError(Exception):
    """Raised by agent-mock when a fixture is configured to raise an error."""

    def __init__(
        self,
        message: str = "Mock error",
        status_code: int = 500,
        type: str = "mock_error",
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.type = type


class _NoMatch(Exception):
    """Internal: raised when strict mode finds no matching fixture."""
    pass


def _dict_to_namespace(obj: Any) -> Any:
    """Recursively convert dicts to SimpleNamespace."""
    if isinstance(obj, dict):
        return types.SimpleNamespace(**{k: _dict_to_namespace(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [_dict_to_namespace(i) for i in obj]
    return obj


def _serialize_response(response: Any) -> Dict:
    if isinstance(response, dict):
        return response
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if hasattr(response, "dict"):
        return response.dict()
    if hasattr(response, "__dict__"):
        return json.loads(json.dumps(vars(response), default=str))
    raise TypeError(f"Cannot serialize response of type {type(response)}")


# Params that identify a request for fixture matching
_MATCH_PARAMS = frozenset({
    "model", "temperature", "max_tokens", "max_tokens_to_sample",
    "top_p", "top_k", "stop_sequences", "stop", "system", "seed",
    "n", "frequency_penalty", "presence_penalty",
})


def _make_key(model: str, messages: Any, **params: Any) -> str:
    match_params = {k: v for k, v in params.items() if k in _MATCH_PARAMS}
    key_obj = {
        "model": model,
        "messages": messages,
        **dict(sorted(match_params.items())),
    }
    serialized = json.dumps(key_obj, sort_keys=True, ensure_ascii=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()


class _Fixture:
    """A single registered fixture."""

    def __init__(
        self,
        key: str,
        responses: List[Any],
        raises: Optional[MockError],
        side_effect: Optional[Callable],
    ):
        self.key = key
        self.responses = responses
        self.raises = raises
        self.side_effect = side_effect
        self._call_count = 0

    def call(self) -> Any:
        self._call_count += 1
        if self.side_effect:
            return self.side_effect(self._call_count)
        if self.raises:
            raise self.raises
        if not self.responses:
            raise MockError(f"No response configured for fixture (key={self.key[:8]})")
        # Cycle through responses list (last one repeats)
        idx = min(self._call_count - 1, len(self.responses) - 1)
        resp = self.responses[idx]
        return _dict_to_namespace(resp) if isinstance(resp, dict) else resp


class _Cassette:
    """A recorded set of API interactions."""

    def __init__(self):
        self._interactions: List[Dict] = []

    def record(self, key: str, request: Dict, response: Dict) -> None:
        self._interactions.append({
            "key": key,
            "request": request,
            "response": response,
        })

    def find(self, key: str) -> Optional[Dict]:
        for interaction in self._interactions:
            if interaction["key"] == key:
                return interaction["response"]
        return None

    def save(self, path: str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f:
            json.dump({"interactions": self._interactions}, f, indent=2)

    @classmethod
    def load(cls, path: str) -> "_Cassette":
        cassette = cls()
        with open(path) as f:
            data = json.load(f)
        cassette._interactions = data.get("interactions", [])
        return cassette

    def __len__(self) -> int:
        return len(self._interactions)


class MockSession:
    """
    Mock LLM responses for testing AI agents.

    Three modes:
    - Fixture mode: pre-define responses for specific requests
    - Record mode: make real API calls and save them to a cassette file
    - Playback mode: replay a saved cassette, no real API calls made

    Usage::

        # Fixture mode
        session = MockSession()
        session.on(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hello"}],
            returns={"content": [{"type": "text", "text": "Hi!"}], ...}
        )
        client = session.wrap(anthropic.Anthropic())
        response = client.messages.create(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "hello"}],
        )
        assert response.content[0].text == "Hi!"

        # Record/playback
        with MockSession.record("cassette.json") as session:
            client = session.wrap(anthropic.Anthropic())
            response = client.messages.create(...)  # real call, saved

        with MockSession.playback("cassette.json") as session:
            client = session.wrap(anthropic.Anthropic())
            response = client.messages.create(...)  # served from cassette
    """

    def __init__(self, strict: bool = False):
        """
        Args:
            strict: If True, raises MockError when a call has no matching fixture.
                    If False (default), passes unmatched calls through to real client.
        """
        self._fixtures: Dict[str, _Fixture] = {}
        self._cassette: Optional[_Cassette] = None
        self._cassette_path: Optional[str] = None
        self._record_mode: bool = False
        self._playback_mode: bool = False
        self.strict = strict
        self._call_count: int = 0

    # ------------------------------------------------------------------
    # Fixture API
    # ------------------------------------------------------------------

    def on(
        self,
        model: str = "",
        messages: Any = None,
        returns: Union[Dict, List[Dict], None] = None,
        raises: Optional[MockError] = None,
        side_effect: Optional[Callable] = None,
        **params: Any,
    ) -> "_MockBuilder":
        """
        Register a fixture response for a specific request.

        Args:
            model: Model name to match (empty = match any)
            messages: Messages list to match (None = match any)
            returns: Response dict or list of dicts (cycled through on repeat calls,
                     last one repeating). Can be a partial response — missing fields
                     are filled in with defaults.
            raises: MockError to raise instead of returning a response.
            side_effect: Callable(call_count) called instead of returning.
            **params: Additional params to match (temperature, max_tokens, etc.)
        """
        if messages is None:
            messages = []
        key = _make_key(model, messages, **params)

        if returns is not None:
            if isinstance(returns, dict):
                responses = [_fill_defaults(returns, model)]
            elif isinstance(returns, list):
                responses = [_fill_defaults(r, model) for r in returns]
            else:
                responses = [returns]
        else:
            responses = []

        self._fixtures[key] = _Fixture(
            key=key,
            responses=responses,
            raises=raises,
            side_effect=side_effect,
        )
        return _MockBuilder(self, key)

    def reset(self) -> None:
        """Clear all fixtures and reset call counts."""
        self._fixtures.clear()
        self._call_count = 0

    @property
    def call_count(self) -> int:
        return self._call_count

    # ------------------------------------------------------------------
    # Record/playback API
    # ------------------------------------------------------------------

    @classmethod
    def record(cls, path: str, strict: bool = False) -> "_RecordContext":
        """Context manager: record real API calls to a cassette file."""
        return _RecordContext(path, strict=strict)

    @classmethod
    def playback(cls, path: str, strict: bool = True) -> "_PlaybackContext":
        """Context manager: replay a cassette, no real API calls made."""
        return _PlaybackContext(path, strict=strict)

    # ------------------------------------------------------------------
    # Client wrapping
    # ------------------------------------------------------------------

    def wrap(self, client: Any) -> Any:
        """
        Wrap an Anthropic or OpenAI client. Returns a mocked client.
        """
        module = type(client).__module__
        if "anthropic" in module:
            from .wrappers import MockedAnthropicClient
            return MockedAnthropicClient(client, self)
        if "openai" in module:
            from .wrappers import MockedOpenAIClient
            return MockedOpenAIClient(client, self)
        raise ValueError(
            f"Unknown client type: {type(client).__name__}. "
            "Pass an anthropic.Anthropic or openai.OpenAI instance."
        )

    # ------------------------------------------------------------------
    # Internal: called by wrappers
    # ------------------------------------------------------------------

    def _handle(
        self,
        model: str,
        messages: Any,
        real_client_fn: Callable,
        **kwargs: Any,
    ) -> Any:
        """Route a call to fixture, cassette, or real client."""
        self._call_count += 1
        key = _make_key(model, messages, **kwargs)

        # Playback: serve from cassette
        if self._playback_mode and self._cassette is not None:
            resp = self._cassette.find(key)
            if resp is not None:
                return _dict_to_namespace(resp)
            if self.strict:
                raise MockError(
                    f"No cassette entry for request (key={key[:8]}). "
                    "Re-record the cassette.",
                    status_code=0,
                    type="cassette_miss",
                )
            # Fall through to real client

        # Fixture match
        fixture = self._fixtures.get(key)
        if fixture is not None:
            return fixture.call()

        if self.strict and not self._record_mode:
            raise MockError(
                f"Unexpected call: model={model!r}, messages={messages!r}. "
                "Add a fixture or disable strict mode.",
                status_code=0,
                type="unexpected_call",
            )

        # Record: make real call and save
        if self._record_mode and self._cassette is not None:
            response = real_client_fn()
            response_dict = _serialize_response(response)
            request_dict = {"model": model, "messages": messages, **kwargs}
            self._cassette.record(key, request_dict, response_dict)
            return response

        # Pass through to real client
        return real_client_fn()

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "MockSession":
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __repr__(self) -> str:
        return (
            f"MockSession(fixtures={len(self._fixtures)}, "
            f"calls={self._call_count}, strict={self.strict})"
        )


class _MockBuilder:
    """Fluent builder returned by MockSession.on() for chaining."""

    def __init__(self, session: MockSession, key: str):
        self._session = session
        self._key = key

    def then(
        self,
        returns: Union[Dict, List[Dict], None] = None,
        raises: Optional[MockError] = None,
    ) -> "_MockBuilder":
        """Add additional responses (called on second, third... invocations)."""
        fixture = self._session._fixtures.get(self._key)
        if fixture is None:
            return self
        if returns is not None:
            if isinstance(returns, dict):
                fixture.responses.append(_fill_defaults(returns, ""))
            elif isinstance(returns, list):
                fixture.responses.extend([_fill_defaults(r, "") for r in returns])
        if raises is not None:
            fixture.raises = raises
        return self


class _RecordContext:
    def __init__(self, path: str, strict: bool = False):
        self._path = path
        self._session: Optional[MockSession] = None
        self._strict = strict

    def __enter__(self) -> MockSession:
        self._session = MockSession(strict=self._strict)
        self._session._record_mode = True
        self._session._cassette = _Cassette()
        self._session._cassette_path = self._path
        return self._session

    def __exit__(self, *_: Any) -> None:
        if self._session and self._session._cassette:
            self._session._cassette.save(self._path)


class _PlaybackContext:
    def __init__(self, path: str, strict: bool = True):
        self._path = path
        self._strict = strict

    def __enter__(self) -> MockSession:
        session = MockSession(strict=self._strict)
        session._playback_mode = True
        session._cassette = _Cassette.load(self._path)
        return session

    def __exit__(self, *_: Any) -> None:
        pass


# ---------------------------------------------------------------------------
# Default response builders
# ---------------------------------------------------------------------------

_ANTHROPIC_DEFAULT = {
    "id": "msg_mock",
    "type": "message",
    "role": "assistant",
    "model": "",
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {"input_tokens": 0, "output_tokens": 0},
    "content": [{"type": "text", "text": ""}],
}

_OPENAI_DEFAULT = {
    "id": "chatcmpl_mock",
    "object": "chat.completion",
    "model": "",
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": ""},
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
}


def _fill_defaults(response: Dict, model: str) -> Dict:
    """Fill in missing fields from a partial response dict."""
    # Detect format by checking for "type": "message" (Anthropic) or "object": "chat.completion" (OpenAI)
    if response.get("type") == "message" or "content" in response:
        base = dict(_ANTHROPIC_DEFAULT)
        base.update(response)
        base["model"] = base.get("model") or model
        return base
    if response.get("object") == "chat.completion" or "choices" in response:
        base = dict(_OPENAI_DEFAULT)
        base.update(response)
        base["model"] = base.get("model") or model
        return base
    # Unknown format — return as-is
    return response
