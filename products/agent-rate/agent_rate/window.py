"""
Sliding window counter rate limiter.

Simpler than token bucket but no burst support.
Tracks timestamps of recent requests in a deque.
"""

import asyncio
import collections
import threading
import time

from .limiter import RateLimitExceeded


class SlidingWindowLimiter:
    """
    Sliding window counter rate limiter.
    Simpler than token bucket but no burst support.

    Tracks timestamps of recent requests in a deque.
    If count of requests in last `window_seconds` >= max_requests, waits.

    Usage:
        limiter = SlidingWindowLimiter(max_requests=50, window_seconds=60)
        limiter.limit()  # waits if needed
        result = client.messages.create(...)
    """

    def __init__(self, max_requests: int, window_seconds: float = 60):
        if max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")

        self._max_requests = max_requests
        self._window = window_seconds
        self._timestamps: collections.deque = collections.deque()
        self._lock = threading.Lock()

    def _evict_old(self, now: float) -> None:
        """Remove timestamps older than the window. Must be called under lock."""
        cutoff = now - self._window
        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()

    def limit(self, block: bool = True) -> float:
        """
        Acquire rate limit permission.

        If block=True: sleeps until a slot is available, returns wait_time.
        If block=False: raises RateLimitExceeded if window is full.

        Returns: time waited in seconds (0 if no wait needed).
        """
        total_wait = 0.0

        while True:
            with self._lock:
                now = time.monotonic()
                self._evict_old(now)

                if len(self._timestamps) < self._max_requests:
                    self._timestamps.append(now)
                    return total_wait

                # Window is full — oldest timestamp tells us when a slot opens
                oldest = self._timestamps[0]
                wait = (oldest + self._window) - now
                # Add a tiny epsilon to ensure the eviction fires after sleep
                wait = max(wait, 0.0) + 1e-6

            if not block:
                raise RateLimitExceeded(retry_after=wait)

            time.sleep(wait)
            total_wait += wait

    async def alimit(self, block: bool = True) -> float:
        """Async version of limit(). Uses asyncio.sleep."""
        total_wait = 0.0

        while True:
            with self._lock:
                now = time.monotonic()
                self._evict_old(now)

                if len(self._timestamps) < self._max_requests:
                    self._timestamps.append(now)
                    return total_wait

                oldest = self._timestamps[0]
                wait = (oldest + self._window) - now
                wait = max(wait, 0.0) + 1e-6

            if not block:
                raise RateLimitExceeded(retry_after=wait)

            await asyncio.sleep(wait)
            total_wait += wait

    @property
    def current_count(self) -> int:
        """Number of requests in the current window."""
        with self._lock:
            self._evict_old(time.monotonic())
            return len(self._timestamps)

    @property
    def remaining(self) -> int:
        """Requests remaining in current window."""
        return max(0, self._max_requests - self.current_count)
