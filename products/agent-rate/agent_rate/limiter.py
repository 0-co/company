"""
Token bucket rate limiter for AI agent API calls.

Supports requests-per-minute and tokens-per-minute limiting,
burst mode, sync/async, decorator, and context manager interfaces.
"""

import asyncio
import functools
import threading
import time


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded and block=False."""

    def __init__(self, retry_after: float):
        self.retry_after = retry_after  # seconds to wait
        super().__init__(
            f"Rate limit exceeded. Retry after {retry_after:.3f}s."
        )


class _TokenBucket:
    """
    Internal token bucket implementation.

    Capacity = burst_factor * rate_per_second
    Refill rate = rate_per_second tokens/sec
    Each call consumes `cost` tokens.
    """

    def __init__(self, rate_per_second: float, burst_factor: float):
        self._rate = rate_per_second  # tokens/sec refill rate
        self._capacity = burst_factor * rate_per_second  # max tokens
        self._tokens = self._capacity  # start full
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        """Refill tokens based on elapsed time. Must be called under lock."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
        self._last_refill = now

    def consume(self, cost: float = 1.0, block: bool = True) -> float:
        """
        Consume `cost` tokens from the bucket.

        Returns seconds waited (0.0 if no wait).
        Raises RateLimitExceeded if block=False and tokens insufficient.
        """
        with self._lock:
            self._refill()
            if self._tokens >= cost:
                self._tokens -= cost
                return 0.0

            # Calculate wait needed to accumulate `cost` tokens
            deficit = cost - self._tokens
            wait = deficit / self._rate

            if not block:
                raise RateLimitExceeded(retry_after=wait)

        # Sleep outside the lock to allow other threads to proceed
        time.sleep(wait)

        with self._lock:
            self._refill()
            # After sleeping, tokens should be sufficient; consume them
            self._tokens = max(0.0, self._tokens - cost)

        return wait

    async def aconsume(self, cost: float = 1.0, block: bool = True) -> float:
        """Async version of consume(). Uses asyncio.sleep."""
        with self._lock:
            self._refill()
            if self._tokens >= cost:
                self._tokens -= cost
                return 0.0

            deficit = cost - self._tokens
            wait = deficit / self._rate

            if not block:
                raise RateLimitExceeded(retry_after=wait)

        await asyncio.sleep(wait)

        with self._lock:
            self._refill()
            self._tokens = max(0.0, self._tokens - cost)

        return wait

    @property
    def available(self) -> float:
        """Current token level (0 to capacity)."""
        with self._lock:
            self._refill()
            return self._tokens

    def reset(self) -> None:
        """Fill bucket to capacity."""
        with self._lock:
            self._tokens = self._capacity
            self._last_refill = time.monotonic()

    @property
    def capacity(self) -> float:
        return self._capacity


class RateLimiter:
    """
    Token bucket rate limiter for API calls.

    Supports:
    - requests per minute limiting
    - tokens per minute limiting (pass token_count to limit())
    - burst mode (allow short bursts up to burst_factor * rate)
    - sync blocking (wait until rate allows)
    - sync non-blocking (raise RateLimitExceeded immediately)
    - async variants

    Usage:
        limiter = RateLimiter(requests_per_minute=50)

        # Blocking (waits if needed)
        limiter.limit()
        result = client.messages.create(...)

        # Non-blocking (raises if would have to wait)
        try:
            limiter.limit(block=False)
        except RateLimitExceeded as e:
            time.sleep(e.retry_after)

        # With token tracking
        limiter = RateLimiter(requests_per_minute=50, tokens_per_minute=100000)
        limiter.limit(token_count=1500)  # consumes 1 request + 1500 tokens

        # Decorator
        @limiter.rate_limited
        def call_llm(messages):
            return client.messages.create(...)

        # Context manager
        with limiter:
            result = client.messages.create(...)
    """

    def __init__(
        self,
        requests_per_minute: float = 60,
        tokens_per_minute: float = None,  # None = no token limiting
        burst_factor: float = 1.5,        # allow brief bursts up to burst_factor * rate
    ):
        if requests_per_minute <= 0:
            raise ValueError("requests_per_minute must be positive")
        if burst_factor <= 0:
            raise ValueError("burst_factor must be positive")

        self._rpm = requests_per_minute
        self._tpm = tokens_per_minute
        self._burst_factor = burst_factor

        # requests bucket: rate = rpm / 60 tokens per second
        self._req_bucket = _TokenBucket(
            rate_per_second=requests_per_minute / 60.0,
            burst_factor=burst_factor,
        )

        # tokens bucket: only created when tpm is specified
        if tokens_per_minute is not None:
            if tokens_per_minute <= 0:
                raise ValueError("tokens_per_minute must be positive")
            self._tok_bucket = _TokenBucket(
                rate_per_second=tokens_per_minute / 60.0,
                burst_factor=burst_factor,
            )
        else:
            self._tok_bucket = None

    def limit(self, token_count: int = 0, block: bool = True) -> float:
        """
        Acquire rate limit permission.

        If block=True: sleeps until permission granted, returns wait_time.
        If block=False: raises RateLimitExceeded if would need to wait > 0.

        token_count: how many tokens this call will use (for TPM limiting).
        Returns: time waited in seconds (0 if no wait needed).
        """
        wait = self._req_bucket.consume(cost=1.0, block=block)

        if self._tok_bucket is not None and token_count > 0:
            tok_wait = self._tok_bucket.consume(cost=float(token_count), block=block)
            wait += tok_wait

        return wait

    async def alimit(self, token_count: int = 0, block: bool = True) -> float:
        """Async version of limit(). Uses asyncio.sleep instead of time.sleep."""
        wait = await self._req_bucket.aconsume(cost=1.0, block=block)

        if self._tok_bucket is not None and token_count > 0:
            tok_wait = await self._tok_bucket.aconsume(
                cost=float(token_count), block=block
            )
            wait += tok_wait

        return wait

    def rate_limited(self, func):
        """Decorator. Calls self.limit() before each invocation."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.limit()
            return func(*args, **kwargs)
        return wrapper

    def rate_limited_async(self, func):
        """Async decorator. Calls self.alimit() before each invocation."""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            await self.alimit()
            return await func(*args, **kwargs)
        return wrapper

    def __enter__(self):
        """Context manager: calls limit()."""
        self.limit()
        return self

    def __exit__(self, *args):
        pass

    @property
    def requests_available(self) -> float:
        """Current token bucket level for requests (0 to burst capacity)."""
        return self._req_bucket.available

    @property
    def tokens_available(self):
        """Current token bucket level for tokens (0 to burst capacity). None if not configured."""
        if self._tok_bucket is None:
            return None
        return self._tok_bucket.available

    def reset(self):
        """Reset the rate limiter (fill buckets to capacity)."""
        self._req_bucket.reset()
        if self._tok_bucket is not None:
            self._tok_bucket.reset()
