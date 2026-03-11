"""
agent-timeout: Zero-dependency timeout and deadline enforcement for AI agent API calls.

Zero external dependencies. Python 3.9+. Cross-platform (no signal.alarm).
Uses threading for sync timeouts, asyncio.wait_for for async.
"""

from .budget import BudgetExhausted, TimeBudget
from .timeout import (
    TimeoutExceeded,
    timeout,
    timeout_async,
    timeout_decorator,
    with_timeout,
    with_timeout_async,
)

__version__ = "0.1.0"
__all__ = [
    "TimeoutExceeded",
    "with_timeout",
    "timeout",
    "timeout_decorator",
    "with_timeout_async",
    "timeout_async",
    "TimeBudget",
    "BudgetExhausted",
]
