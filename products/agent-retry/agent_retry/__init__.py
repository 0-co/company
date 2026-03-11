"""
agent-retry — retry logic for AI agent API calls.

Zero dependencies. Pure stdlib. Works with sync and async.

Quick start::

    from agent_retry import retry

    @retry(max_attempts=3, base_delay=1.0)
    def call_claude():
        return client.messages.create(...)

    # Async works the same way
    @retry(max_attempts=3)
    async def async_call():
        return await client.messages.create(...)

    # RetryConfig for full control
    from agent_retry import RetryConfig

    config = RetryConfig(
        max_attempts=5,
        base_delay=2.0,
        max_delay=30.0,
        jitter=True,
        on_retry=lambda attempt, exc, delay: print(f"Retry {attempt} in {delay:.1f}s: {exc}"),
    )

    @retry(config=config)
    def call_openai():
        ...
"""

from .exceptions import RetryExhausted
from .retry import (
    DEFAULT_NON_RETRYABLE_STATUS_CODES,
    DEFAULT_RETRYABLE_STATUS_CODES,
    RetryConfig,
    retry,
)

__version__ = "0.1.0"

__all__ = [
    "retry",
    "RetryConfig",
    "RetryExhausted",
    "DEFAULT_RETRYABLE_STATUS_CODES",
    "DEFAULT_NON_RETRYABLE_STATUS_CODES",
]
