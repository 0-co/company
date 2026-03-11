"""
HealthChecker: core health check logic.
Runs probes, tracks history, provides status and background watching.
"""

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional

from .probe import Probe


class HealthStatus(str, Enum):
    """
    UP        — probe succeeded within latency thresholds
    DEGRADED  — probe succeeded but latency exceeded degraded_threshold_ms
    DOWN      — probe failed (exception raised)
    UNKNOWN   — no checks have been run yet
    """

    UP = "up"
    DEGRADED = "degraded"
    DOWN = "down"
    UNKNOWN = "unknown"


@dataclass
class HealthResult:
    """Result of a single health probe execution."""

    status: HealthStatus
    latency_ms: float
    error: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    @property
    def is_healthy(self) -> bool:
        return self.status in (HealthStatus.UP, HealthStatus.DEGRADED)

    def __repr__(self) -> str:
        if self.error:
            return f"HealthResult({self.status.value}, {self.latency_ms:.1f}ms, error={self.error!r})"
        return f"HealthResult({self.status.value}, {self.latency_ms:.1f}ms)"


class HealthChecker:
    """
    Runs a probe on demand or in the background and tracks health status.

    Usage::

        from agent_health import HealthChecker, AnthropicProbe

        probe = AnthropicProbe(client)
        checker = HealthChecker(probe)

        result = checker.check()
        print(result.status)   # HealthStatus.UP

        # Background polling
        checker.start_watching(interval=30)
        print(checker.status)  # latest cached status

        # Gate a function
        @checker.requires_healthy
        def call_api():
            ...

    Parameters
    ----------
    probe:
        A callable that returns (success, latency_ms, error). Any Probe subclass works,
        or any callable matching that signature.
    degraded_threshold_ms:
        Latency above this is DEGRADED rather than UP. Default: 3000ms.
    history_size:
        How many results to keep. Default: 100.
    name:
        Optional display name (used in HealthPool).
    """

    def __init__(
        self,
        probe: Probe,
        degraded_threshold_ms: float = 3000.0,
        history_size: int = 100,
        name: str = "",
    ):
        self.probe = probe
        self.degraded_threshold_ms = degraded_threshold_ms
        self.history_size = history_size
        self.name = name

        self._history: List[HealthResult] = []
        self._lock = threading.Lock()
        self._watcher_thread: Optional[threading.Thread] = None
        self._watching = False

    # ------------------------------------------------------------------
    # Core API

    def check(self) -> HealthResult:
        """
        Run the probe once synchronously and return the result.
        Also appends to history.
        """
        success, latency_ms, error = self.probe()

        if not success:
            status = HealthStatus.DOWN
        elif latency_ms > self.degraded_threshold_ms:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UP

        result = HealthResult(status=status, latency_ms=latency_ms, error=error)

        with self._lock:
            self._history.append(result)
            if len(self._history) > self.history_size:
                self._history = self._history[-self.history_size :]

        return result

    @property
    def status(self) -> HealthStatus:
        """Latest known status. UNKNOWN if no checks have run."""
        with self._lock:
            if not self._history:
                return HealthStatus.UNKNOWN
            return self._history[-1].status

    @property
    def latest(self) -> Optional[HealthResult]:
        """Most recent HealthResult, or None."""
        with self._lock:
            return self._history[-1] if self._history else None

    @property
    def history(self) -> List[HealthResult]:
        """Copy of the results history (oldest first)."""
        with self._lock:
            return list(self._history)

    @property
    def is_healthy(self) -> bool:
        """True if status is UP or DEGRADED (not DOWN or UNKNOWN)."""
        return self.status in (HealthStatus.UP, HealthStatus.DEGRADED)

    # ------------------------------------------------------------------
    # Statistics

    def success_rate(self, last_n: Optional[int] = None) -> float:
        """
        Fraction of recent checks that were UP or DEGRADED.
        Returns 0.0 if no checks yet.
        """
        with self._lock:
            window = self._history[-last_n:] if last_n else self._history
        if not window:
            return 0.0
        healthy = sum(1 for r in window if r.is_healthy)
        return healthy / len(window)

    def average_latency_ms(self, last_n: Optional[int] = None) -> float:
        """Average latency over recent checks. 0.0 if no checks."""
        with self._lock:
            window = self._history[-last_n:] if last_n else self._history
        if not window:
            return 0.0
        return sum(r.latency_ms for r in window) / len(window)

    def p95_latency_ms(self, last_n: Optional[int] = None) -> float:
        """95th percentile latency. 0.0 if fewer than 2 checks."""
        with self._lock:
            window = self._history[-last_n:] if last_n else self._history
        if len(window) < 2:
            return 0.0
        sorted_latencies = sorted(r.latency_ms for r in window)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[min(idx, len(sorted_latencies) - 1)]

    # ------------------------------------------------------------------
    # Background watching

    def start_watching(
        self,
        interval: float = 30.0,
        on_status_change: Optional[Callable[["HealthChecker", HealthResult], None]] = None,
    ) -> None:
        """
        Start a background daemon thread that calls check() every `interval` seconds.

        Parameters
        ----------
        interval:
            Seconds between checks.
        on_status_change:
            Optional callback invoked whenever status transitions (e.g., UP → DOWN).
            Signature: fn(checker, result).
        """
        if self._watching:
            return

        self._watching = True

        def _loop():
            previous_status = self.status
            while self._watching:
                result = self.check()
                if on_status_change and result.status != previous_status:
                    try:
                        on_status_change(self, result)
                    except Exception:
                        pass
                previous_status = result.status
                # Sleep in small increments so we can respond to stop_watching quickly
                deadline = time.monotonic() + interval
                while time.monotonic() < deadline and self._watching:
                    time.sleep(0.1)

        self._watcher_thread = threading.Thread(target=_loop, daemon=True)
        self._watcher_thread.start()

    def stop_watching(self) -> None:
        """Stop the background watcher thread."""
        self._watching = False
        if self._watcher_thread:
            self._watcher_thread.join(timeout=1.0)
            self._watcher_thread = None

    # ------------------------------------------------------------------
    # Decorator

    def requires_healthy(self, fn: Callable) -> Callable:
        """
        Decorator: raises RuntimeError if the checker is not healthy when called.
        Does NOT run a probe on each call — checks the cached status.
        Use with start_watching() for continuous background checks.

        Example::

            @checker.requires_healthy
            def call_api():
                return client.messages.create(...)
        """
        import functools

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            current = self.status
            if current == HealthStatus.UNKNOWN:
                # Run one check if we've never checked
                result = self.check()
                if not result.is_healthy:
                    raise RuntimeError(
                        f"Health check failed before calling {fn.__name__!r}: "
                        f"status={result.status.value}, error={result.error}"
                    )
            elif current == HealthStatus.DOWN:
                raise RuntimeError(
                    f"Service is DOWN, refusing to call {fn.__name__!r}"
                )
            return fn(*args, **kwargs)

        return wrapper

    def __repr__(self) -> str:
        name = f" name={self.name!r}" if self.name else ""
        return f"HealthChecker({self.status.value}{name})"
