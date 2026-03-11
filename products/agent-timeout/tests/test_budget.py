"""
Tests for agent_timeout.budget module.
"""

import time
import unittest

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_timeout import BudgetExhausted, TimeBudget
from agent_timeout import TimeoutExceeded, with_timeout


class TestTimeBudgetBasics(unittest.TestCase):
    """Tests for basic TimeBudget behavior."""

    def test_fresh_budget_remaining_approx_total(self):
        budget = TimeBudget(total_seconds=60.0)
        self.assertAlmostEqual(budget.remaining(), 60.0, delta=0.1)

    def test_elapsed_increases_over_time(self):
        budget = TimeBudget(total_seconds=60.0)
        time.sleep(0.05)
        self.assertGreater(budget.elapsed(), 0.0)

    def test_remaining_decreases_over_time(self):
        budget = TimeBudget(total_seconds=60.0)
        r1 = budget.remaining()
        time.sleep(0.05)
        r2 = budget.remaining()
        self.assertLess(r2, r1)

    def test_is_exhausted_false_for_fresh_budget(self):
        budget = TimeBudget(total_seconds=60.0)
        self.assertFalse(budget.is_exhausted)

    def test_is_exhausted_true_after_budget_expires(self):
        budget = TimeBudget(total_seconds=0.05)
        time.sleep(0.1)
        self.assertTrue(budget.is_exhausted)

    def test_remaining_returns_zero_not_negative(self):
        budget = TimeBudget(total_seconds=0.01)
        time.sleep(0.1)
        self.assertEqual(budget.remaining(), 0.0)

    def test_elapsed_tracks_wall_time_not_cpu_time(self):
        """elapsed() should track wall clock time, not CPU time."""
        budget = TimeBudget(total_seconds=10.0)
        time.sleep(0.1)  # sleep releases CPU — wall time increases, CPU time does not
        elapsed = budget.elapsed()
        self.assertGreaterEqual(elapsed, 0.09)

    def test_total_attribute_stored(self):
        budget = TimeBudget(total_seconds=45.0)
        self.assertEqual(budget.total, 45.0)


class TestTimeBudgetCheck(unittest.TestCase):
    """Tests for TimeBudget.check()."""

    def test_check_passes_when_budget_has_time_left(self):
        budget = TimeBudget(total_seconds=60.0)
        # Should not raise
        budget.check()

    def test_check_raises_budget_exhausted_when_expired(self):
        budget = TimeBudget(total_seconds=0.01)
        time.sleep(0.05)
        with self.assertRaises(BudgetExhausted):
            budget.check()

    def test_budget_exhausted_has_budget_attribute(self):
        budget = TimeBudget(total_seconds=0.01)
        time.sleep(0.05)
        try:
            budget.check()
            self.fail("Expected BudgetExhausted")
        except BudgetExhausted as e:
            self.assertEqual(e.budget, 0.01)

    def test_budget_exhausted_has_elapsed_attribute(self):
        budget = TimeBudget(total_seconds=0.01)
        time.sleep(0.05)
        try:
            budget.check()
            self.fail("Expected BudgetExhausted")
        except BudgetExhausted as e:
            self.assertGreater(e.elapsed, 0.01)

    def test_budget_exhausted_message(self):
        budget = TimeBudget(total_seconds=0.01)
        time.sleep(0.05)
        try:
            budget.check()
            self.fail("Expected BudgetExhausted")
        except BudgetExhausted as e:
            msg = str(e)
            self.assertIn("exhausted", msg.lower())


class TestTimeBudgetTimeoutFor(unittest.TestCase):
    """Tests for TimeBudget.timeout_for()."""

    def test_returns_per_call_when_budget_is_large(self):
        budget = TimeBudget(total_seconds=60.0)
        result = budget.timeout_for(20.0)
        self.assertAlmostEqual(result, 20.0, delta=0.1)

    def test_returns_remaining_when_per_call_exceeds_remaining(self):
        budget = TimeBudget(total_seconds=5.0)
        time.sleep(0.1)
        remaining = budget.remaining()
        result = budget.timeout_for(60.0)
        # Should return remaining, which is < 60
        self.assertLess(result, 60.0)
        self.assertAlmostEqual(result, remaining, delta=0.05)

    def test_raises_budget_exhausted_when_already_exhausted(self):
        budget = TimeBudget(total_seconds=0.01)
        time.sleep(0.05)
        with self.assertRaises(BudgetExhausted):
            budget.timeout_for(20.0)

    def test_multiple_calls_track_correctly(self):
        budget = TimeBudget(total_seconds=60.0)
        t1 = budget.timeout_for(10.0)
        time.sleep(0.02)
        t2 = budget.timeout_for(10.0)
        # Both calls should return <= 10.0, second slightly less remaining
        self.assertLessEqual(t1, 10.0)
        self.assertLessEqual(t2, 10.0)
        # Second call should have slightly less time remaining
        self.assertLessEqual(t2, t1)

    def test_timeout_for_with_zero_per_call_raises_on_exhausted(self):
        budget = TimeBudget(total_seconds=0.01)
        time.sleep(0.05)
        with self.assertRaises(BudgetExhausted):
            budget.timeout_for(0.0)


class TestTimeBudgetReset(unittest.TestCase):
    """Tests for TimeBudget.reset()."""

    def test_reset_resets_elapsed_to_zero(self):
        budget = TimeBudget(total_seconds=60.0)
        time.sleep(0.05)
        elapsed_before = budget.elapsed()
        budget.reset()
        elapsed_after = budget.elapsed()
        self.assertGreater(elapsed_before, elapsed_after)
        self.assertAlmostEqual(elapsed_after, 0.0, delta=0.05)

    def test_reset_makes_exhausted_budget_fresh(self):
        budget = TimeBudget(total_seconds=0.01)
        time.sleep(0.05)
        self.assertTrue(budget.is_exhausted)
        budget.reset()
        self.assertFalse(budget.is_exhausted)

    def test_reset_preserves_total(self):
        budget = TimeBudget(total_seconds=30.0)
        budget.reset()
        self.assertEqual(budget.total, 30.0)


class TestBudgetExhaustedAttributes(unittest.TestCase):
    """Tests for BudgetExhausted exception."""

    def test_has_budget_attribute(self):
        exc = BudgetExhausted(budget=60.0, elapsed=65.0)
        self.assertEqual(exc.budget, 60.0)

    def test_has_elapsed_attribute(self):
        exc = BudgetExhausted(budget=60.0, elapsed=65.0)
        self.assertEqual(exc.elapsed, 65.0)

    def test_is_exception(self):
        exc = BudgetExhausted(budget=60.0, elapsed=65.0)
        self.assertIsInstance(exc, Exception)


class TestTimeBudgetIntegration(unittest.TestCase):
    """Integration tests combining TimeBudget with with_timeout."""

    def test_budget_caps_total_retry_time(self):
        """Budget correctly limits total time across multiple with_timeout calls."""
        budget = TimeBudget(total_seconds=0.5)
        attempts = 0
        caught_budget_exhausted = False

        for _ in range(10):
            try:
                per_call = budget.timeout_for(0.1)
                with_timeout(per_call, time.sleep, 0.3)  # always times out
                attempts += 1
            except TimeoutExceeded:
                attempts += 1
                continue
            except BudgetExhausted:
                caught_budget_exhausted = True
                break

        self.assertTrue(caught_budget_exhausted, "Budget should have been exhausted")
        # Should have completed a few attempts before exhaustion, not all 10
        self.assertLess(attempts, 10)

    def test_budget_allows_completion_within_budget(self):
        """Fast operations complete without exhausting budget."""
        budget = TimeBudget(total_seconds=5.0)
        results = []

        for _ in range(3):
            per_call = budget.timeout_for(2.0)
            result = with_timeout(per_call, lambda: 42)
            results.append(result)

        self.assertEqual(results, [42, 42, 42])
        self.assertFalse(budget.is_exhausted)


if __name__ == "__main__":
    unittest.main()
