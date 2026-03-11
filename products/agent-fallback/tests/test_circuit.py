"""Tests for agent_fallback.circuit."""

import sys
import os
import time
import threading
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_fallback.circuit import CircuitBreaker, CircuitOpen


class TestCircuitBreakerBasic(unittest.TestCase):

    def test_fresh_circuit_is_closed(self):
        cb = CircuitBreaker()
        self.assertFalse(cb.is_open)

    def test_cooldown_remaining_is_zero_when_closed(self):
        cb = CircuitBreaker()
        self.assertEqual(cb.cooldown_remaining, 0.0)

    def test_record_failure_below_threshold_still_closed(self):
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        self.assertFalse(cb.is_open)

    def test_record_failure_at_threshold_opens_circuit(self):
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        cb.record_failure()
        self.assertTrue(cb.is_open)

    def test_is_open_true_after_opening(self):
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure()
        self.assertTrue(cb.is_open)

    def test_cooldown_remaining_positive_when_open(self):
        cb = CircuitBreaker(failure_threshold=1, cooldown_seconds=60)
        cb.record_failure()
        self.assertGreater(cb.cooldown_remaining, 0.0)

    def test_enter_raises_circuit_open_when_open(self):
        cb = CircuitBreaker(failure_threshold=1, name="test-provider")
        cb.record_failure()
        with self.assertRaises(CircuitOpen):
            cb.__enter__()

    def test_circuit_open_has_provider_name(self):
        cb = CircuitBreaker(failure_threshold=1, name="my-provider")
        cb.record_failure()
        try:
            with cb:
                pass
        except CircuitOpen as exc:
            self.assertEqual(exc.provider_name, "my-provider")

    def test_circuit_open_has_cooldown_remaining(self):
        cb = CircuitBreaker(failure_threshold=1, cooldown_seconds=60)
        cb.record_failure()
        try:
            with cb:
                pass
        except CircuitOpen as exc:
            self.assertGreater(exc.cooldown_remaining, 0.0)

    def test_record_success_resets_failure_count(self):
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        cb.record_success()
        # Failure count reset — need to reach threshold again
        cb.record_failure()
        self.assertFalse(cb.is_open)

    def test_record_success_after_open_closes_circuit(self):
        cb = CircuitBreaker(failure_threshold=2)
        cb.record_failure()
        cb.record_failure()
        self.assertTrue(cb.is_open)
        cb.record_success()
        self.assertFalse(cb.is_open)

    def test_reset_forces_closed_state(self):
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure()
        self.assertTrue(cb.is_open)
        cb.reset()
        self.assertFalse(cb.is_open)

    def test_circuit_auto_resets_after_cooldown(self):
        cb = CircuitBreaker(failure_threshold=1, cooldown_seconds=0.05)
        cb.record_failure()
        self.assertTrue(cb.is_open)
        time.sleep(0.1)
        self.assertFalse(cb.is_open)

    def test_failure_threshold_1_opens_after_first_failure(self):
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure()
        self.assertTrue(cb.is_open)

    def test_context_manager_records_failure_on_exception(self):
        cb = CircuitBreaker(failure_threshold=2)
        try:
            with cb:
                raise ValueError("test error")
        except ValueError:
            pass
        # One failure recorded
        self.assertFalse(cb.is_open)  # threshold is 2, only 1 failure
        cb.record_failure()  # second failure
        self.assertTrue(cb.is_open)

    def test_context_manager_records_success_when_no_exception(self):
        cb = CircuitBreaker(failure_threshold=2)
        cb.record_failure()  # one failure
        with cb:
            pass  # no exception
        # Success resets count — now needs 2 fresh failures to open
        cb.record_failure()
        self.assertFalse(cb.is_open)

    def test_context_manager_does_not_suppress_exceptions(self):
        cb = CircuitBreaker(failure_threshold=3)
        with self.assertRaises(RuntimeError):
            with cb:
                raise RuntimeError("should propagate")

    def test_context_manager_enter_raises_circuit_open_when_open(self):
        cb = CircuitBreaker(failure_threshold=1, name="p")
        cb.record_failure()
        with self.assertRaises(CircuitOpen):
            with cb:
                pass  # should not reach here

    def test_cooldown_remaining_decreases_over_time(self):
        cb = CircuitBreaker(failure_threshold=1, cooldown_seconds=1.0)
        cb.record_failure()
        r1 = cb.cooldown_remaining
        time.sleep(0.05)
        r2 = cb.cooldown_remaining
        self.assertGreater(r1, r2)

    def test_circuit_stays_open_until_cooldown_elapses(self):
        cb = CircuitBreaker(failure_threshold=1, cooldown_seconds=0.1)
        cb.record_failure()
        # Should still be open immediately after
        self.assertTrue(cb.is_open)
        time.sleep(0.15)
        self.assertFalse(cb.is_open)

    def test_thread_safety_concurrent_failures(self):
        """Multiple threads recording failures should not corrupt state."""
        cb = CircuitBreaker(failure_threshold=10, cooldown_seconds=10)
        errors = []

        def fail_once():
            try:
                cb.record_failure()
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=fail_once) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])
        self.assertTrue(cb.is_open)


if __name__ == "__main__":
    unittest.main()
