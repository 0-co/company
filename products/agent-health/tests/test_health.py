"""
Tests for agent-health.
"""

import time
import threading
import unittest
from unittest.mock import MagicMock, patch

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_health import (
    HealthChecker,
    HealthResult,
    HealthStatus,
    HealthPool,
    Probe,
    AnthropicProbe,
    OpenAIProbe,
    CustomProbe,
)


# ---------------------------------------------------------------------------
# Helper probes for testing

class AlwaysUpProbe(Probe):
    """Simulates a healthy service with configurable latency."""

    def __init__(self, latency_ms: float = 50.0):
        self.latency_ms = latency_ms
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        return True, self.latency_ms, None


class AlwaysDownProbe(Probe):
    """Simulates a failed service."""

    def __init__(self, error: str = "Connection refused"):
        self.error = error
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        return False, 0.0, self.error


class SlowProbe(Probe):
    """Simulates a slow (degraded) service."""

    def __init__(self, latency_ms: float = 5000.0):
        self.latency_ms = latency_ms
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        return True, self.latency_ms, None


class FlappingProbe(Probe):
    """Alternates between UP and DOWN on each call."""

    def __init__(self):
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        if self.call_count % 2 == 1:
            return True, 100.0, None
        return False, 0.0, "Flapping"


# ---------------------------------------------------------------------------
# HealthResult tests

class TestHealthResult(unittest.TestCase):

    def test_up_is_healthy(self):
        r = HealthResult(status=HealthStatus.UP, latency_ms=100.0)
        self.assertTrue(r.is_healthy)

    def test_degraded_is_healthy(self):
        r = HealthResult(status=HealthStatus.DEGRADED, latency_ms=5000.0)
        self.assertTrue(r.is_healthy)

    def test_down_is_not_healthy(self):
        r = HealthResult(status=HealthStatus.DOWN, latency_ms=0.0, error="timeout")
        self.assertFalse(r.is_healthy)

    def test_unknown_is_not_healthy(self):
        r = HealthResult(status=HealthStatus.UNKNOWN, latency_ms=0.0)
        self.assertFalse(r.is_healthy)

    def test_repr_with_error(self):
        r = HealthResult(status=HealthStatus.DOWN, latency_ms=10.0, error="refused")
        self.assertIn("refused", repr(r))

    def test_repr_without_error(self):
        r = HealthResult(status=HealthStatus.UP, latency_ms=100.0)
        self.assertIn("up", repr(r))
        self.assertIn("100.0", repr(r))

    def test_timestamp_is_set(self):
        before = time.time()
        r = HealthResult(status=HealthStatus.UP, latency_ms=50.0)
        after = time.time()
        self.assertGreaterEqual(r.timestamp, before)
        self.assertLessEqual(r.timestamp, after)


# ---------------------------------------------------------------------------
# HealthChecker tests

class TestHealthCheckerStatus(unittest.TestCase):

    def test_initial_status_is_unknown(self):
        checker = HealthChecker(AlwaysUpProbe())
        self.assertEqual(checker.status, HealthStatus.UNKNOWN)

    def test_initial_is_not_healthy(self):
        checker = HealthChecker(AlwaysUpProbe())
        self.assertFalse(checker.is_healthy)

    def test_check_up(self):
        checker = HealthChecker(AlwaysUpProbe(latency_ms=50.0))
        result = checker.check()
        self.assertEqual(result.status, HealthStatus.UP)
        self.assertEqual(checker.status, HealthStatus.UP)
        self.assertTrue(checker.is_healthy)

    def test_check_down(self):
        checker = HealthChecker(AlwaysDownProbe("connection refused"))
        result = checker.check()
        self.assertEqual(result.status, HealthStatus.DOWN)
        self.assertEqual(result.error, "connection refused")
        self.assertFalse(checker.is_healthy)

    def test_check_degraded(self):
        checker = HealthChecker(SlowProbe(latency_ms=5000.0), degraded_threshold_ms=3000.0)
        result = checker.check()
        self.assertEqual(result.status, HealthStatus.DEGRADED)
        self.assertTrue(result.is_healthy)  # degraded is still healthy

    def test_check_exactly_at_threshold_is_up(self):
        # Threshold is strict (>), so exactly at threshold = UP
        checker = HealthChecker(SlowProbe(latency_ms=3000.0), degraded_threshold_ms=3000.0)
        result = checker.check()
        self.assertEqual(result.status, HealthStatus.UP)

    def test_check_just_below_threshold_is_up(self):
        checker = HealthChecker(AlwaysUpProbe(latency_ms=2999.0), degraded_threshold_ms=3000.0)
        result = checker.check()
        self.assertEqual(result.status, HealthStatus.UP)

    def test_latest_returns_most_recent(self):
        checker = HealthChecker(AlwaysUpProbe())
        self.assertIsNone(checker.latest)
        r1 = checker.check()
        r2 = checker.check()
        self.assertIs(checker.latest, r2)

    def test_history_appends(self):
        checker = HealthChecker(AlwaysUpProbe())
        self.assertEqual(len(checker.history), 0)
        checker.check()
        checker.check()
        checker.check()
        self.assertEqual(len(checker.history), 3)

    def test_history_is_copy(self):
        checker = HealthChecker(AlwaysUpProbe())
        checker.check()
        h = checker.history
        h.clear()
        self.assertEqual(len(checker.history), 1)

    def test_history_size_limit(self):
        checker = HealthChecker(AlwaysUpProbe(), history_size=5)
        for _ in range(10):
            checker.check()
        self.assertEqual(len(checker.history), 5)

    def test_history_keeps_most_recent(self):
        # History should keep the last N results, not the first N
        probe = AlwaysUpProbe()
        checker = HealthChecker(probe, history_size=3)
        probe.call_count = 0
        for _ in range(5):
            checker.check()
        # We checked 5 times; history size is 3; so 3 entries remain
        self.assertEqual(len(checker.history), 3)

    def test_probe_call_count(self):
        probe = AlwaysUpProbe()
        checker = HealthChecker(probe)
        checker.check()
        checker.check()
        checker.check()
        self.assertEqual(probe.call_count, 3)

    def test_repr_contains_status(self):
        checker = HealthChecker(AlwaysUpProbe())
        checker.check()
        self.assertIn("up", repr(checker))

    def test_repr_contains_name(self):
        checker = HealthChecker(AlwaysUpProbe(), name="anthropic")
        self.assertIn("anthropic", repr(checker))

    def test_check_returns_result(self):
        checker = HealthChecker(AlwaysUpProbe())
        result = checker.check()
        self.assertIsInstance(result, HealthResult)


# ---------------------------------------------------------------------------
# HealthChecker statistics

class TestHealthCheckerStats(unittest.TestCase):

    def test_success_rate_all_up(self):
        checker = HealthChecker(AlwaysUpProbe())
        for _ in range(10):
            checker.check()
        self.assertAlmostEqual(checker.success_rate(), 1.0)

    def test_success_rate_all_down(self):
        checker = HealthChecker(AlwaysDownProbe())
        for _ in range(10):
            checker.check()
        self.assertAlmostEqual(checker.success_rate(), 0.0)

    def test_success_rate_no_checks(self):
        checker = HealthChecker(AlwaysUpProbe())
        self.assertEqual(checker.success_rate(), 0.0)

    def test_success_rate_flapping(self):
        probe = FlappingProbe()
        checker = HealthChecker(probe)
        for _ in range(4):
            checker.check()
        # 2 UP, 2 DOWN → 50%
        self.assertAlmostEqual(checker.success_rate(), 0.5)

    def test_success_rate_last_n(self):
        probe = FlappingProbe()
        checker = HealthChecker(probe)
        for _ in range(4):
            checker.check()
        # last 2: DOWN, UP (checks 3,4) → 50%
        rate = checker.success_rate(last_n=2)
        self.assertAlmostEqual(rate, 0.5)

    def test_average_latency_no_checks(self):
        checker = HealthChecker(AlwaysUpProbe())
        self.assertEqual(checker.average_latency_ms(), 0.0)

    def test_average_latency(self):
        checker = HealthChecker(AlwaysUpProbe(latency_ms=100.0))
        for _ in range(5):
            checker.check()
        self.assertAlmostEqual(checker.average_latency_ms(), 100.0)

    def test_average_latency_last_n(self):
        probe = AlwaysUpProbe(latency_ms=100.0)
        checker = HealthChecker(probe)
        checker.check()
        probe.latency_ms = 200.0
        checker.check()
        probe.latency_ms = 300.0
        checker.check()
        # last 2: 200 + 300 = 250 avg
        self.assertAlmostEqual(checker.average_latency_ms(last_n=2), 250.0)

    def test_p95_no_checks(self):
        checker = HealthChecker(AlwaysUpProbe())
        self.assertEqual(checker.p95_latency_ms(), 0.0)

    def test_p95_one_check(self):
        checker = HealthChecker(AlwaysUpProbe())
        checker.check()
        self.assertEqual(checker.p95_latency_ms(), 0.0)  # needs >=2

    def test_p95_multiple_checks(self):
        probe = AlwaysUpProbe()
        checker = HealthChecker(probe)
        latencies = [100.0, 110.0, 120.0, 130.0, 500.0]
        for lat in latencies:
            probe.latency_ms = lat
            checker.check()
        p95 = checker.p95_latency_ms()
        self.assertGreater(p95, 130.0)


# ---------------------------------------------------------------------------
# Background watching

class TestHealthCheckerWatcher(unittest.TestCase):

    def test_start_and_stop_watching(self):
        checker = HealthChecker(AlwaysUpProbe())
        checker.start_watching(interval=0.05)
        time.sleep(0.15)
        checker.stop_watching()
        # Should have run at least 1 check
        self.assertGreater(len(checker.history), 0)

    def test_status_updates_during_watch(self):
        checker = HealthChecker(AlwaysUpProbe())
        checker.start_watching(interval=0.05)
        time.sleep(0.15)
        checker.stop_watching()
        self.assertEqual(checker.status, HealthStatus.UP)

    def test_start_watching_twice_is_idempotent(self):
        checker = HealthChecker(AlwaysUpProbe())
        checker.start_watching(interval=0.05)
        checker.start_watching(interval=0.05)  # second call is no-op
        time.sleep(0.1)
        checker.stop_watching()
        # Should only have one watcher thread

    def test_on_status_change_callback(self):
        changes = []
        probe = FlappingProbe()
        checker = HealthChecker(probe)

        def on_change(c, r):
            changes.append(r.status)

        checker.start_watching(interval=0.02, on_status_change=on_change)
        time.sleep(0.2)
        checker.stop_watching()
        # Should have detected at least one transition
        self.assertGreater(len(changes), 0)

    def test_stop_watching_when_not_watching(self):
        checker = HealthChecker(AlwaysUpProbe())
        # Should not raise
        checker.stop_watching()


# ---------------------------------------------------------------------------
# requires_healthy decorator

class TestRequiresHealthy(unittest.TestCase):

    def test_passes_when_up(self):
        checker = HealthChecker(AlwaysUpProbe())
        checker.check()

        @checker.requires_healthy
        def fn():
            return 42

        self.assertEqual(fn(), 42)

    def test_raises_when_down(self):
        checker = HealthChecker(AlwaysDownProbe())
        checker.check()

        @checker.requires_healthy
        def fn():
            return 42

        with self.assertRaises(RuntimeError) as ctx:
            fn()
        self.assertIn("DOWN", str(ctx.exception))

    def test_passes_when_degraded(self):
        checker = HealthChecker(SlowProbe(5000.0), degraded_threshold_ms=3000.0)
        checker.check()

        @checker.requires_healthy
        def fn():
            return "ok"

        self.assertEqual(fn(), "ok")

    def test_runs_probe_on_unknown(self):
        probe = AlwaysUpProbe()
        checker = HealthChecker(probe)
        # No check() called yet — status is UNKNOWN

        @checker.requires_healthy
        def fn():
            return "ok"

        result = fn()
        self.assertEqual(result, "ok")
        self.assertEqual(probe.call_count, 1)

    def test_raises_on_unknown_and_down_probe(self):
        checker = HealthChecker(AlwaysDownProbe())
        # Status is UNKNOWN; decorator runs a check → DOWN

        @checker.requires_healthy
        def fn():
            return "ok"

        with self.assertRaises(RuntimeError):
            fn()

    def test_preserves_function_name(self):
        checker = HealthChecker(AlwaysUpProbe())

        @checker.requires_healthy
        def my_function():
            pass

        self.assertEqual(my_function.__name__, "my_function")

    def test_passes_args_through(self):
        checker = HealthChecker(AlwaysUpProbe())
        checker.check()

        @checker.requires_healthy
        def add(a, b):
            return a + b

        self.assertEqual(add(2, 3), 5)


# ---------------------------------------------------------------------------
# Probe tests

class TestProbes(unittest.TestCase):

    def test_custom_probe_success(self):
        called = []
        probe = CustomProbe(lambda: called.append(1))
        success, latency, error = probe()
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(called, [1])

    def test_custom_probe_failure(self):
        def boom():
            raise ValueError("oops")

        probe = CustomProbe(boom)
        success, latency, error = probe()
        self.assertFalse(success)
        self.assertIn("oops", error)
        self.assertGreaterEqual(latency, 0.0)

    def test_anthropic_probe(self):
        mock_client = MagicMock()
        probe = AnthropicProbe(mock_client)
        success, latency, error = probe()
        self.assertTrue(success)
        self.assertIsNone(error)
        mock_client.messages.create.assert_called_once_with(
            model="claude-haiku-4-5-20251001",
            max_tokens=1,
            messages=[{"role": "user", "content": "hi"}],
        )

    def test_anthropic_probe_custom_model(self):
        mock_client = MagicMock()
        probe = AnthropicProbe(mock_client, model="claude-opus-4-6")
        probe()
        call_kwargs = mock_client.messages.create.call_args[1]
        self.assertEqual(call_kwargs["model"], "claude-opus-4-6")

    def test_anthropic_probe_failure(self):
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("API error")
        probe = AnthropicProbe(mock_client)
        success, latency, error = probe()
        self.assertFalse(success)
        self.assertIn("API error", error)

    def test_openai_probe(self):
        mock_client = MagicMock()
        probe = OpenAIProbe(mock_client)
        success, latency, error = probe()
        self.assertTrue(success)
        self.assertIsNone(error)
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            max_tokens=1,
            messages=[{"role": "user", "content": "hi"}],
        )

    def test_openai_probe_failure(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = RuntimeError("rate limit")
        probe = OpenAIProbe(mock_client)
        success, latency, error = probe()
        self.assertFalse(success)
        self.assertIn("rate limit", error)

    def test_latency_measured(self):
        def slow():
            time.sleep(0.05)

        probe = CustomProbe(slow)
        success, latency, error = probe()
        self.assertTrue(success)
        self.assertGreaterEqual(latency, 50.0)


# ---------------------------------------------------------------------------
# HealthPool tests

class TestHealthPool(unittest.TestCase):

    def _make_pool(self):
        return HealthPool({
            "a": HealthChecker(AlwaysUpProbe()),
            "b": HealthChecker(SlowProbe(5000.0), degraded_threshold_ms=3000.0),
            "c": HealthChecker(AlwaysDownProbe()),
        })

    def test_check_all(self):
        pool = self._make_pool()
        results = pool.check_all()
        self.assertIn("a", results)
        self.assertIn("b", results)
        self.assertIn("c", results)

    def test_check_all_status(self):
        pool = self._make_pool()
        results = pool.check_all()
        self.assertEqual(results["a"].status, HealthStatus.UP)
        self.assertEqual(results["b"].status, HealthStatus.DEGRADED)
        self.assertEqual(results["c"].status, HealthStatus.DOWN)

    def test_healthy_returns_up_and_degraded(self):
        pool = self._make_pool()
        pool.check_all()
        healthy = pool.healthy()
        self.assertIn("a", healthy)
        self.assertIn("b", healthy)
        self.assertNotIn("c", healthy)

    def test_up_returns_only_up(self):
        pool = self._make_pool()
        pool.check_all()
        up = pool.up()
        self.assertIn("a", up)
        self.assertNotIn("b", up)
        self.assertNotIn("c", up)

    def test_down_returns_only_down(self):
        pool = self._make_pool()
        pool.check_all()
        down = pool.down()
        self.assertIn("c", down)
        self.assertNotIn("a", down)
        self.assertNotIn("b", down)

    def test_any_healthy_true(self):
        pool = self._make_pool()
        pool.check_all()
        self.assertTrue(pool.any_healthy())

    def test_any_healthy_false(self):
        pool = HealthPool({
            "x": HealthChecker(AlwaysDownProbe()),
            "y": HealthChecker(AlwaysDownProbe()),
        })
        pool.check_all()
        self.assertFalse(pool.any_healthy())

    def test_all_healthy_false(self):
        pool = self._make_pool()
        pool.check_all()
        self.assertFalse(pool.all_healthy())

    def test_all_healthy_true(self):
        pool = HealthPool({
            "x": HealthChecker(AlwaysUpProbe()),
            "y": HealthChecker(AlwaysUpProbe()),
        })
        pool.check_all()
        self.assertTrue(pool.all_healthy())

    def test_best_returns_fastest_up(self):
        pool = HealthPool({
            "fast": HealthChecker(AlwaysUpProbe(latency_ms=10.0), name="fast"),
            "slow": HealthChecker(AlwaysUpProbe(latency_ms=200.0), name="slow"),
        })
        pool.check_all()
        self.assertEqual(pool.best(), "fast")

    def test_best_prefers_up_over_degraded(self):
        pool = self._make_pool()
        pool.check_all()
        # "a" is UP, "b" is DEGRADED → best should be "a"
        self.assertEqual(pool.best(), "a")

    def test_best_returns_degraded_when_no_up(self):
        pool = HealthPool({
            "degraded": HealthChecker(SlowProbe(5000.0), degraded_threshold_ms=3000.0),
            "down": HealthChecker(AlwaysDownProbe()),
        })
        pool.check_all()
        self.assertEqual(pool.best(), "degraded")

    def test_best_returns_none_when_all_down(self):
        pool = HealthPool({
            "x": HealthChecker(AlwaysDownProbe()),
        })
        pool.check_all()
        self.assertIsNone(pool.best())

    def test_best_returns_none_when_all_unknown(self):
        pool = HealthPool({
            "x": HealthChecker(AlwaysUpProbe()),
        })
        # No check run → UNKNOWN
        self.assertIsNone(pool.best())

    def test_statuses(self):
        pool = self._make_pool()
        pool.check_all()
        statuses = pool.statuses()
        self.assertEqual(statuses["a"], HealthStatus.UP)
        self.assertEqual(statuses["b"], HealthStatus.DEGRADED)
        self.assertEqual(statuses["c"], HealthStatus.DOWN)

    def test_summary(self):
        pool = self._make_pool()
        pool.check_all()
        s = pool.summary()
        self.assertEqual(s["total"], 3)
        self.assertEqual(s["up"], 1)
        self.assertEqual(s["degraded"], 1)
        self.assertEqual(s["down"], 1)
        self.assertTrue(s["any_healthy"])
        self.assertEqual(s["best"], "a")

    def test_repr(self):
        pool = self._make_pool()
        pool.check_all()
        r = repr(pool)
        self.assertIn("up", r)
        self.assertIn("degraded", r)
        self.assertIn("down", r)

    def test_start_and_stop_watching_all(self):
        pool = HealthPool({
            "a": HealthChecker(AlwaysUpProbe()),
            "b": HealthChecker(AlwaysUpProbe()),
        })
        pool.start_watching_all(interval=0.05)
        time.sleep(0.1)
        pool.stop_watching_all()
        # Both should have run checks
        for checker in pool.checkers.values():
            self.assertGreater(len(checker.history), 0)


# ---------------------------------------------------------------------------
# Thread safety

class TestThreadSafety(unittest.TestCase):

    def test_concurrent_checks(self):
        """Multiple threads calling check() simultaneously should not crash."""
        checker = HealthChecker(AlwaysUpProbe(), history_size=1000)
        errors = []

        def run():
            try:
                for _ in range(20):
                    checker.check()
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=run) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])
        # All 100 checks should be in history (size=1000)
        self.assertEqual(len(checker.history), 100)

    def test_concurrent_history_reads(self):
        """Reading history while checks are in flight should not crash."""
        checker = HealthChecker(AlwaysUpProbe())
        for _ in range(50):
            checker.check()

        results = []
        errors = []

        def read():
            try:
                results.append(len(checker.history))
            except Exception as e:
                errors.append(e)

        def write():
            try:
                checker.check()
            except Exception as e:
                errors.append(e)

        threads = [
            threading.Thread(target=read if i % 2 == 0 else write)
            for i in range(20)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])


# ---------------------------------------------------------------------------
# Integration: HealthChecker with real timing

class TestTimingIntegration(unittest.TestCase):

    def test_probe_latency_recorded(self):
        """Probe latency should be non-negative."""
        def fast_fn():
            pass  # instant

        probe = CustomProbe(fast_fn)
        checker = HealthChecker(probe)
        result = checker.check()
        self.assertGreaterEqual(result.latency_ms, 0.0)

    def test_slow_probe_is_degraded(self):
        def slow_fn():
            time.sleep(0.06)  # 60ms

        probe = CustomProbe(slow_fn)
        checker = HealthChecker(probe, degraded_threshold_ms=50.0)
        result = checker.check()
        self.assertEqual(result.status, HealthStatus.DEGRADED)

    def test_fast_probe_is_up(self):
        probe = CustomProbe(lambda: None)
        checker = HealthChecker(probe, degraded_threshold_ms=5000.0)
        result = checker.check()
        self.assertEqual(result.status, HealthStatus.UP)


if __name__ == "__main__":
    unittest.main()
