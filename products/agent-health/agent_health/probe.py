"""
Probe strategies for health checking different AI APIs.
A probe makes a lightweight call and returns (success, latency_ms, error).
"""

import time
from typing import Callable, Optional, Tuple


class Probe:
    """Base probe class. Override _execute() for custom behavior."""

    def __call__(self) -> Tuple[bool, float, Optional[str]]:
        """
        Execute the probe.
        Returns: (success, latency_ms, error_message_or_None)
        """
        start = time.monotonic()
        try:
            self._execute()
            latency_ms = (time.monotonic() - start) * 1000
            return True, latency_ms, None
        except Exception as e:
            latency_ms = (time.monotonic() - start) * 1000
            return False, latency_ms, str(e)

    def _execute(self) -> None:
        raise NotImplementedError


class AnthropicProbe(Probe):
    """
    Probes an Anthropic client with a minimal completion call.
    Uses the cheapest/fastest available model by default.
    """

    def __init__(self, client, model: str = "claude-haiku-4-5-20251001"):
        self.client = client
        self.model = model

    def _execute(self) -> None:
        self.client.messages.create(
            model=self.model,
            max_tokens=1,
            messages=[{"role": "user", "content": "hi"}],
        )


class OpenAIProbe(Probe):
    """
    Probes an OpenAI client with a minimal completion call.
    Uses gpt-3.5-turbo by default (cheapest/fastest).
    """

    def __init__(self, client, model: str = "gpt-3.5-turbo"):
        self.client = client
        self.model = model

    def _execute(self) -> None:
        self.client.chat.completions.create(
            model=self.model,
            max_tokens=1,
            messages=[{"role": "user", "content": "hi"}],
        )


class CustomProbe(Probe):
    """
    Wrap any callable as a probe.
    The callable should raise on failure, or return normally on success.

    Example:
        probe = CustomProbe(lambda: requests.get("https://api.example.com/health").raise_for_status())
    """

    def __init__(self, fn: Callable[[], None]):
        self._fn = fn

    def _execute(self) -> None:
        self._fn()
