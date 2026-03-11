"""
HealthPool: manage and query health across multiple providers/endpoints.
Pairs naturally with agent-fallback — use a pool to pick healthy providers.
"""

from typing import Dict, List, Optional

from .checker import HealthChecker, HealthResult, HealthStatus


class HealthPool:
    """
    A named collection of HealthCheckers.

    Usage::

        from agent_health import HealthPool, HealthChecker, AnthropicProbe, OpenAIProbe

        pool = HealthPool({
            "anthropic": HealthChecker(AnthropicProbe(anthropic_client), name="anthropic"),
            "openai":    HealthChecker(OpenAIProbe(openai_client),    name="openai"),
        })

        # Check all
        results = pool.check_all()

        # Get only healthy ones
        healthy = pool.healthy()  # list of names with UP/DEGRADED status

        # Check if any are available
        if pool.any_healthy():
            name = pool.best()  # name of healthiest (UP preferred over DEGRADED)
    """

    def __init__(self, checkers: Dict[str, HealthChecker]):
        self.checkers = checkers

    # ------------------------------------------------------------------
    # Collective operations

    def check_all(self) -> Dict[str, HealthResult]:
        """Run check() on all checkers and return name → result mapping."""
        return {name: checker.check() for name, checker in self.checkers.items()}

    def start_watching_all(self, interval: float = 30.0) -> None:
        """Start background watchers on all checkers."""
        for checker in self.checkers.values():
            checker.start_watching(interval=interval)

    def stop_watching_all(self) -> None:
        """Stop background watchers on all checkers."""
        for checker in self.checkers.values():
            checker.stop_watching()

    # ------------------------------------------------------------------
    # Query

    def healthy(self) -> List[str]:
        """Names of checkers with status UP or DEGRADED."""
        return [
            name
            for name, checker in self.checkers.items()
            if checker.is_healthy
        ]

    def up(self) -> List[str]:
        """Names of checkers with status exactly UP."""
        return [
            name
            for name, checker in self.checkers.items()
            if checker.status == HealthStatus.UP
        ]

    def down(self) -> List[str]:
        """Names of checkers with status DOWN."""
        return [
            name
            for name, checker in self.checkers.items()
            if checker.status == HealthStatus.DOWN
        ]

    def any_healthy(self) -> bool:
        """True if at least one checker is UP or DEGRADED."""
        return any(c.is_healthy for c in self.checkers.values())

    def all_healthy(self) -> bool:
        """True if all checkers are UP or DEGRADED."""
        return all(c.is_healthy for c in self.checkers.values())

    def best(self) -> Optional[str]:
        """
        Return the name of the 'best' available checker:
        1. Any UP checker with the lowest average latency
        2. If none UP, any DEGRADED checker
        3. None if all DOWN or UNKNOWN

        Useful for routing: pick the fastest healthy provider.
        """
        up_checkers = [
            (name, checker)
            for name, checker in self.checkers.items()
            if checker.status == HealthStatus.UP
        ]
        if up_checkers:
            return min(up_checkers, key=lambda nc: nc[1].average_latency_ms())[0]

        degraded_checkers = [
            (name, checker)
            for name, checker in self.checkers.items()
            if checker.status == HealthStatus.DEGRADED
        ]
        if degraded_checkers:
            return min(degraded_checkers, key=lambda nc: nc[1].average_latency_ms())[0]

        return None

    def statuses(self) -> Dict[str, HealthStatus]:
        """Current status of all checkers."""
        return {name: checker.status for name, checker in self.checkers.items()}

    def summary(self) -> Dict[str, object]:
        """
        A summary dict suitable for logging/dashboards.
        """
        total = len(self.checkers)
        n_up = len(self.up())
        n_degraded = sum(
            1 for c in self.checkers.values() if c.status == HealthStatus.DEGRADED
        )
        n_down = len(self.down())
        return {
            "total": total,
            "up": n_up,
            "degraded": n_degraded,
            "down": n_down,
            "any_healthy": self.any_healthy(),
            "best": self.best(),
            "statuses": {n: c.status.value for n, c in self.checkers.items()},
        }

    def __repr__(self) -> str:
        summary = self.statuses()
        parts = ", ".join(f"{n}={s.value}" for n, s in summary.items())
        return f"HealthPool({parts})"
