"""
TimeBudget — total time budget tracking across multiple operations/retries.

Useful when retrying API calls — prevents exceeding a total wall-clock budget
even if each individual call stays within its per-call timeout.
"""

import time


class BudgetExhausted(Exception):
    """Raised when the total time budget is exhausted."""

    def __init__(self, budget: float, elapsed: float):
        self.budget = budget
        self.elapsed = elapsed
        super().__init__(
            f"Time budget exhausted: {elapsed:.1f}s elapsed, budget was {budget}s"
        )


class TimeBudget:
    """
    Track total time budget across multiple operations/retries.

    Useful when retrying API calls — you don't want to exceed a total budget
    even if each individual call stays within its per-call timeout.

    Example::

        from agent_timeout import TimeBudget, with_timeout, TimeoutExceeded

        budget = TimeBudget(total_seconds=60)  # 1 minute total

        for attempt in range(3):
            try:
                per_call = budget.timeout_for(20)  # at most 20s, or remaining budget
                result = with_timeout(per_call, call_llm, messages)
                break
            except TimeoutExceeded:
                continue

    Args:
        total_seconds: Total wall-clock seconds available across all operations.
    """

    def __init__(self, total_seconds: float):
        self.total = total_seconds
        self._start = time.monotonic()

    def elapsed(self) -> float:
        """Seconds elapsed since budget was created."""
        return time.monotonic() - self._start

    def remaining(self) -> float:
        """Seconds remaining in budget. Returns 0.0 if exhausted."""
        rem = self.total - self.elapsed()
        return max(0.0, rem)

    def check(self):
        """
        Raises BudgetExhausted if remaining() <= 0.

        Call this before starting a new operation to fail fast.
        """
        elapsed = self.elapsed()
        if elapsed >= self.total:
            raise BudgetExhausted(self.total, elapsed)

    def timeout_for(self, per_call_seconds: float) -> float:
        """
        Returns min(per_call_seconds, remaining()).

        Use this to get the actual timeout for the next call so you never
        exceed the total budget even with per-call limits.

        Args:
            per_call_seconds: The desired per-call timeout.

        Returns:
            The actual timeout to use: min(per_call_seconds, remaining()).

        Raises:
            BudgetExhausted: If the budget is already exhausted.
        """
        self.check()
        return min(per_call_seconds, self.remaining())

    def reset(self):
        """Reset the budget timer (start fresh with the same total)."""
        self._start = time.monotonic()

    @property
    def is_exhausted(self) -> bool:
        """True if remaining() <= 0."""
        return self.remaining() <= 0
