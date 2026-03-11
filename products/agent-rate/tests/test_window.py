"""
Tests for SlidingWindowLimiter.

Uses short windows (e.g. 0.1s) to test eviction without long sleeps.
"""

import asyncio
import time
import unittest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_rate import SlidingWindowLimiter, RateLimitExceeded


class TestSlidingWindowLimiterInit(unittest.TestCase):

    def test_fresh_window_count_is_zero(self):
        limiter = SlidingWindowLimiter(max_requests=10, window_seconds=60)
        self.assertEqual(limiter.current_count, 0)

    def test_remaining_equals_max_initially(self):
        limiter = SlidingWindowLimiter(max_requests=10, window_seconds=60)
        self.assertEqual(limiter.remaining, 10)

    def test_invalid_max_requests_raises(self):
        with self.assertRaises(ValueError):
            SlidingWindowLimiter(max_requests=0)
        with self.assertRaises(ValueError):
            SlidingWindowLimiter(max_requests=-5)

    def test_invalid_window_seconds_raises(self):
        with self.assertRaises(ValueError):
            SlidingWindowLimiter(max_requests=10, window_seconds=0)
        with self.assertRaises(ValueError):
            SlidingWindowLimiter(max_requests=10, window_seconds=-1)


class TestSlidingWindowLimiterLimit(unittest.TestCase):

    def test_limit_returns_zero_for_first_requests(self):
        limiter = SlidingWindowLimiter(max_requests=5, window_seconds=60)
        for _ in range(5):
            wait = limiter.limit()
            self.assertEqual(wait, 0.0)

    def test_current_count_increments_on_each_call(self):
        limiter = SlidingWindowLimiter(max_requests=10, window_seconds=60)
        for i in range(1, 5):
            limiter.limit()
            self.assertEqual(limiter.current_count, i)

    def test_remaining_decrements_correctly(self):
        limiter = SlidingWindowLimiter(max_requests=5, window_seconds=60)
        self.assertEqual(limiter.remaining, 5)
        limiter.limit()
        self.assertEqual(limiter.remaining, 4)
        limiter.limit()
        self.assertEqual(limiter.remaining, 3)

    def test_limit_raises_when_window_full_nonblock(self):
        limiter = SlidingWindowLimiter(max_requests=3, window_seconds=60)
        limiter.limit()
        limiter.limit()
        limiter.limit()
        with self.assertRaises(RateLimitExceeded) as ctx:
            limiter.limit(block=False)
        self.assertGreater(ctx.exception.retry_after, 0)

    def test_rate_limit_exceeded_retry_after_positive(self):
        limiter = SlidingWindowLimiter(max_requests=1, window_seconds=60)
        limiter.limit()
        try:
            limiter.limit(block=False)
            self.fail("Expected RateLimitExceeded")
        except RateLimitExceeded as e:
            self.assertGreater(e.retry_after, 0)
            self.assertLessEqual(e.retry_after, 60 + 0.01)

    def test_old_requests_evicted_after_window(self):
        """Use a very short window so we can test eviction without long sleeps."""
        limiter = SlidingWindowLimiter(max_requests=2, window_seconds=0.1)
        limiter.limit()
        limiter.limit()
        # Both slots are full — next non-blocking should raise
        with self.assertRaises(RateLimitExceeded):
            limiter.limit(block=False)
        # Wait for window to expire
        time.sleep(0.15)
        # Now both old entries should be evicted
        self.assertEqual(limiter.current_count, 0)
        wait = limiter.limit()
        self.assertEqual(wait, 0.0)

    def test_blocking_limit_waits_for_slot(self):
        """Short window: blocking limit should wait and succeed."""
        limiter = SlidingWindowLimiter(max_requests=1, window_seconds=0.1)
        limiter.limit()  # fills the window
        # Blocking call should sleep ~0.1s and then succeed
        start = time.monotonic()
        wait = limiter.limit(block=True)
        elapsed = time.monotonic() - start
        self.assertGreater(wait, 0.0)
        self.assertLess(elapsed, 0.5)  # must not take more than 0.5s

    def test_remaining_never_goes_below_zero(self):
        limiter = SlidingWindowLimiter(max_requests=2, window_seconds=60)
        limiter.limit()
        limiter.limit()
        self.assertEqual(limiter.remaining, 0)

    def test_current_count_after_eviction(self):
        """After window expires, current_count should reflect only recent reqs."""
        limiter = SlidingWindowLimiter(max_requests=3, window_seconds=0.1)
        limiter.limit()
        limiter.limit()
        time.sleep(0.15)  # let old entries expire
        # count should be 0 now; new requests start fresh
        limiter.limit()
        self.assertEqual(limiter.current_count, 1)


class TestSlidingWindowLimiterAsync(unittest.TestCase):

    def test_alimit_basic_happy_path(self):
        limiter = SlidingWindowLimiter(max_requests=5, window_seconds=60)

        async def run():
            return await limiter.alimit()

        wait = asyncio.get_event_loop().run_until_complete(run())
        self.assertEqual(wait, 0.0)

    def test_alimit_raises_when_full_nonblock(self):
        limiter = SlidingWindowLimiter(max_requests=2, window_seconds=60)
        limiter.limit()
        limiter.limit()

        async def run():
            await limiter.alimit(block=False)

        with self.assertRaises(RateLimitExceeded):
            asyncio.get_event_loop().run_until_complete(run())

    def test_alimit_multiple_calls(self):
        limiter = SlidingWindowLimiter(max_requests=5, window_seconds=60)

        async def run():
            results = []
            for _ in range(3):
                w = await limiter.alimit()
                results.append(w)
            return results

        waits = asyncio.get_event_loop().run_until_complete(run())
        self.assertEqual(len(waits), 3)
        for w in waits:
            self.assertEqual(w, 0.0)

    def test_alimit_blocking_waits_for_slot(self):
        """Async blocking call should wait for window to expire."""
        limiter = SlidingWindowLimiter(max_requests=1, window_seconds=0.1)
        limiter.limit()

        async def run():
            return await limiter.alimit(block=True)

        start = time.monotonic()
        wait = asyncio.get_event_loop().run_until_complete(run())
        elapsed = time.monotonic() - start
        self.assertGreater(wait, 0.0)
        self.assertLess(elapsed, 0.5)


if __name__ == "__main__":
    unittest.main()
