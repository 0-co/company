"""
Circuit breaker for agent-fallback.

Prevents hammering a known-dead provider by opening the circuit
after too many failures and auto-resetting after a cooldown period.

States:
  CLOSED — normal operation, requests go through
  OPEN   — too many failures, requests immediately raise CircuitOpen
           (auto-resets to CLOSED after cooldown_seconds)
"""

import threading
import time


class CircuitOpen(Exception):
    """Raised when a circuit breaker is open (provider is in cooldown)."""

    def __init__(self, provider_name: str, cooldown_remaining: float):
        self.provider_name = provider_name
        self.cooldown_remaining = cooldown_remaining
        super().__init__(
            f"Circuit for '{provider_name}' is open. "
            f"Cooldown: {cooldown_remaining:.1f}s remaining."
        )


class CircuitBreaker:
    """
    Simple circuit breaker for a single provider.

    After failure_threshold consecutive failures, the circuit opens.
    While open, any attempt to use the breaker raises CircuitOpen.
    After cooldown_seconds have passed since the last failure,
    the circuit auto-resets to closed.

    Usage::

        breaker = CircuitBreaker(failure_threshold=3, cooldown_seconds=60)

        try:
            with breaker:           # raises CircuitOpen if open
                result = call_api()
            breaker.record_success()
        except CircuitOpen:
            pass  # skip this provider, try fallback

    The context-manager form automatically records failures/successes:

    - If an exception is raised inside the ``with`` block, ``record_failure``
      is called before the exception propagates.
    - If the block exits cleanly, ``record_success`` is called.

    You can also call ``record_failure`` / ``record_success`` manually if you
    prefer not to use the context manager.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        cooldown_seconds: float = 60.0,
        name: str = "",
    ):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.name = name or "provider"

        self._failures: int = 0
        self._last_failure_time: float = 0.0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_open(self) -> bool:
        """True if circuit is open (provider in cooldown)."""
        with self._lock:
            return self._is_open_locked()

    def _is_open_locked(self) -> bool:
        """Must be called while holding self._lock."""
        if self._failures < self.failure_threshold:
            return False
        # Check whether cooldown has elapsed — if so, auto-reset.
        elapsed = time.monotonic() - self._last_failure_time
        if elapsed >= self.cooldown_seconds:
            # Auto-reset
            self._failures = 0
            self._last_failure_time = 0.0
            return False
        return True

    @property
    def cooldown_remaining(self) -> float:
        """Seconds until circuit auto-resets. 0.0 if circuit is closed."""
        with self._lock:
            if not self._is_open_locked():
                return 0.0
            elapsed = time.monotonic() - self._last_failure_time
            remaining = self.cooldown_seconds - elapsed
            return max(0.0, remaining)

    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------

    def record_failure(self) -> None:
        """Increment failure count. If >= threshold, open the circuit."""
        with self._lock:
            self._failures += 1
            self._last_failure_time = time.monotonic()

    def record_success(self) -> None:
        """Reset failure count and close the circuit."""
        with self._lock:
            self._failures = 0
            self._last_failure_time = 0.0

    def reset(self) -> None:
        """Force reset to closed state regardless of current status."""
        with self._lock:
            self._failures = 0
            self._last_failure_time = 0.0

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "CircuitBreaker":
        """Raises CircuitOpen if circuit is open."""
        with self._lock:
            if self._is_open_locked():
                elapsed = time.monotonic() - self._last_failure_time
                remaining = max(0.0, self.cooldown_seconds - elapsed)
                raise CircuitOpen(
                    provider_name=self.name,
                    cooldown_remaining=remaining,
                )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Record failure if exception raised inside block, success if clean exit."""
        if exc_type is not None and not issubclass(exc_type, CircuitOpen):
            self.record_failure()
        elif exc_type is None:
            self.record_success()
        # Do not suppress any exception
        return False
