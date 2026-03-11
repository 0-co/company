"""
Core fallback logic for agent-fallback.

Provides:
  - Provider — dataclass describing one LLM provider
  - FallbackResult — wraps the response with metadata
  - ProviderFailed — raised when all providers are exhausted
  - Fallback — tries providers in order until one succeeds
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Set


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ProviderFailed(Exception):
    """Raised when all providers have been exhausted."""

    def __init__(self, errors: list):
        self.errors = errors  # list of (provider_name, exception) tuples
        super().__init__(f"All {len(errors)} providers failed")


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------

class FallbackResult:
    """Result from a Fallback.complete() call."""

    def __init__(self, response: Any, provider: "Provider", attempt: int):
        self.response = response          # raw client response
        self.provider = provider          # which provider succeeded
        self.attempt = attempt            # 1-indexed attempt number
        self.provider_name = provider.name

    def text(self) -> str:
        """
        Extract text from response.

        Handles:
        - Anthropic SDK: response.content[0].text
        - OpenAI SDK: response.choices[0].message.content
        """
        # Anthropic format
        content = getattr(self.response, "content", None)
        if content is not None and len(content) > 0:
            first = content[0]
            text_attr = getattr(first, "text", None)
            if text_attr is not None:
                return text_attr

        # OpenAI format
        choices = getattr(self.response, "choices", None)
        if choices is not None and len(choices) > 0:
            first_choice = choices[0]
            message = getattr(first_choice, "message", None)
            if message is not None:
                msg_content = getattr(message, "content", None)
                if msg_content is not None:
                    return msg_content

        # Fallback: str representation
        return str(self.response)


# ---------------------------------------------------------------------------
# Provider
# ---------------------------------------------------------------------------

@dataclass
class Provider:
    """An LLM provider to try."""
    client: Any                 # Anthropic or OpenAI client instance
    model: str                  # model name to use with this client
    name: str = ""              # friendly name for logging/debugging
    max_tokens: int = 1024

    def __post_init__(self):
        if not self.name:
            self.name = self.model


# ---------------------------------------------------------------------------
# Fallback
# ---------------------------------------------------------------------------

# Default HTTP status codes that indicate the provider is down or overloaded,
# making it worth trying the next provider in the chain.
DEFAULT_RETRYABLE_STATUS_CODES: Set[int] = {500, 502, 503, 529}

# HTTP status codes that mean the *request* is wrong or we are not
# authenticated — trying a different provider won't fix these.
# 429 = rate-limited: the provider IS up, just throttling us.
NON_RETRYABLE_STATUS_CODES: Set[int] = {400, 401, 403, 413, 429}


def _get_status_code(exc: Exception) -> Optional[int]:
    """Extract an HTTP status code from an exception, if present."""
    for attr in ("status_code", "code"):
        code = getattr(exc, attr, None)
        if isinstance(code, int):
            return code
    response = getattr(exc, "response", None)
    if response is not None:
        code = getattr(response, "status_code", None)
        if isinstance(code, int):
            return code
    return None


def _is_anthropic_client(client: Any) -> bool:
    """Detect whether client is an Anthropic client (has .messages attribute)."""
    return hasattr(client, "messages")


def _call_anthropic(provider: Provider, messages: list, system: Optional[str], extra_params: dict) -> Any:
    """Make an Anthropic-style API call."""
    kwargs: dict = {
        "model": provider.model,
        "max_tokens": provider.max_tokens,
        "messages": messages,
    }
    if system is not None:
        kwargs["system"] = system
    kwargs.update(extra_params)
    return provider.client.messages.create(**kwargs)


def _call_openai(provider: Provider, messages: list, system: Optional[str], extra_params: dict) -> Any:
    """Make an OpenAI-style API call."""
    # OpenAI format: system message is prepended as {"role": "system", "content": "..."}
    full_messages = []
    if system is not None:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)

    kwargs: dict = {
        "model": provider.model,
        "messages": full_messages,
        "max_tokens": provider.max_tokens,
    }
    kwargs.update(extra_params)
    return provider.client.chat.completions.create(**kwargs)


class Fallback:
    """
    Try providers in order until one succeeds.

    Usage::

        fb = Fallback([
            Provider(anthropic_client, "claude-sonnet-4-6", name="anthropic"),
            Provider(openai_client, "gpt-4o", name="openai"),
        ])
        result = fb.complete(messages, system="You are helpful.")
        print(result.provider_name, result.text())

    Retryable errors (will try next provider):
    - HTTP 500, 502, 503, 529 from any provider
    - ConnectionError, TimeoutError, OSError (network issues)

    Non-retryable errors (raises immediately without trying next):
    - HTTP 400, 401, 403 (auth/request errors)
    - HTTP 429 (rate limit — means provider is up, just throttling)
    """

    def __init__(
        self,
        providers: List[Provider],
        retryable_status_codes: Optional[Set[int]] = None,
        on_fallback: Optional[Callable] = None,
    ):
        if not providers:
            raise ValueError("At least one provider is required")
        self.providers = providers
        self.retryable_status_codes = (
            retryable_status_codes
            if retryable_status_codes is not None
            else DEFAULT_RETRYABLE_STATUS_CODES
        )
        self.on_fallback = on_fallback

    def complete(
        self,
        messages: list,
        system: Optional[str] = None,
        extra_params: Optional[dict] = None,
    ) -> FallbackResult:
        """
        Try each provider in order. Return first success.

        Raises ProviderFailed if all providers fail with retryable errors.
        Re-raises immediately for non-retryable errors.
        """
        if extra_params is None:
            extra_params = {}

        errors: list = []

        for attempt, provider in enumerate(self.providers, start=1):
            try:
                response = self._call_provider(provider, messages, system, extra_params)
                return FallbackResult(response=response, provider=provider, attempt=attempt)
            except Exception as exc:
                if not self._is_retryable(exc):
                    raise

                errors.append((provider.name, exc))

                # Invoke callback before moving to next provider (if not last)
                if self.on_fallback is not None and attempt < len(self.providers):
                    self.on_fallback(provider, exc)

        raise ProviderFailed(errors=errors)

    async def acomplete(
        self,
        messages: list,
        system: Optional[str] = None,
        extra_params: Optional[dict] = None,
    ) -> FallbackResult:
        """Async version of complete()."""
        if extra_params is None:
            extra_params = {}

        errors: list = []

        for attempt, provider in enumerate(self.providers, start=1):
            try:
                response = await self._acall_provider(provider, messages, system, extra_params)
                return FallbackResult(response=response, provider=provider, attempt=attempt)
            except Exception as exc:
                if not self._is_retryable(exc):
                    raise

                errors.append((provider.name, exc))

                if self.on_fallback is not None and attempt < len(self.providers):
                    self.on_fallback(provider, exc)

        raise ProviderFailed(errors=errors)

    def _is_retryable(self, exc: Exception) -> bool:
        """
        Returns True if we should try the next provider.

        - Network errors (ConnectionError, TimeoutError, OSError, IOError): retryable
        - HTTP 500/502/503/529: retryable
        - HTTP 400/401/403/429: NOT retryable
        - Anything else: NOT retryable
        """
        # Network-level errors are always retryable
        if isinstance(exc, (ConnectionError, TimeoutError, OSError, IOError)):
            return True

        status_code = _get_status_code(exc)

        if status_code is not None:
            # Non-retryable codes take priority
            if status_code in NON_RETRYABLE_STATUS_CODES:
                return False
            # Explicitly retryable codes
            if status_code in self.retryable_status_codes:
                return True
            # Unknown status code — not retryable
            return False

        # No status code, not a network error — not retryable
        return False

    def _call_provider(
        self,
        provider: Provider,
        messages: list,
        system: Optional[str],
        extra_params: dict,
    ) -> Any:
        """Make the actual API call. Detects Anthropic vs OpenAI via hasattr."""
        if _is_anthropic_client(provider.client):
            return _call_anthropic(provider, messages, system, extra_params)
        else:
            return _call_openai(provider, messages, system, extra_params)

    async def _acall_provider(
        self,
        provider: Provider,
        messages: list,
        system: Optional[str],
        extra_params: dict,
    ) -> Any:
        """Async API call. Tries async method first, falls back to sync."""
        # Try async Anthropic
        if _is_anthropic_client(provider.client):
            messages_obj = provider.client.messages
            if hasattr(messages_obj, "acreate"):
                kwargs: dict = {
                    "model": provider.model,
                    "max_tokens": provider.max_tokens,
                    "messages": messages,
                }
                if system is not None:
                    kwargs["system"] = system
                kwargs.update(extra_params)
                return await messages_obj.acreate(**kwargs)
        else:
            # Try async OpenAI
            chat = getattr(provider.client, "chat", None)
            if chat is not None:
                completions = getattr(chat, "completions", None)
                if completions is not None and hasattr(completions, "acreate"):
                    full_messages = []
                    if system is not None:
                        full_messages.append({"role": "system", "content": system})
                    full_messages.extend(messages)
                    kwargs = {
                        "model": provider.model,
                        "messages": full_messages,
                        "max_tokens": provider.max_tokens,
                    }
                    kwargs.update(extra_params)
                    return await completions.acreate(**kwargs)

        # Fall back to running sync call in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self._call_provider(provider, messages, system, extra_params),
        )
