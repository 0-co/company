"""
Core timeout primitives for AI agent API calls.

Uses threading.Thread + join for cross-platform compatibility.
Works on Windows, macOS, Linux. Works in non-main threads.
No signal.alarm (Unix main-thread only).
"""

import asyncio
import functools
import threading
import time


class TimeoutExceeded(Exception):
    """Raised when a timeout is exceeded."""

    def __init__(self, seconds: float, elapsed: float):
        self.seconds = seconds
        self.elapsed = elapsed
        super().__init__(
            f"Operation timed out after {elapsed:.1f}s (limit: {seconds}s)"
        )


def with_timeout(seconds: float, func, *args, **kwargs):
    """
    Run func(*args, **kwargs) with a timeout.
    Raises TimeoutExceeded if it doesn't complete in time.

    Uses threading.Thread + join for cross-platform (works on Windows too).
    Safe for IO-bound operations (LLM API calls, etc).

    Args:
        seconds: Maximum seconds to wait.
        func: Callable to run.
        *args: Positional arguments for func.
        **kwargs: Keyword arguments for func.

    Returns:
        Return value of func.

    Raises:
        TimeoutExceeded: If func does not complete within seconds.
        Exception: Any exception raised by func is re-raised.
    """
    if seconds <= 0:
        raise TimeoutExceeded(seconds, 0.0)

    result = [None]
    exception = [None]

    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target, daemon=True)
    start = time.monotonic()
    thread.start()
    thread.join(timeout=seconds)
    elapsed = time.monotonic() - start

    if thread.is_alive():
        raise TimeoutExceeded(seconds, elapsed)
    if exception[0] is not None:
        raise exception[0]
    return result[0]


class timeout:
    """
    Context manager for timeouts.

    Example::

        with timeout(30):
            result = call_llm(messages)

    Raises:
        TimeoutExceeded: If the body does not complete within the given seconds.
    """

    def __init__(self, seconds: float):
        self.seconds = seconds
        self._thread = None
        self._start = None
        self._timed_out = False

    def __enter__(self):
        self._start = time.monotonic()
        self._timer = _TimeoutTimer(self.seconds, self)
        self._timer.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._timer.cancel()
        if self._timed_out and exc_type is None:
            elapsed = time.monotonic() - self._start
            raise TimeoutExceeded(self.seconds, elapsed)
        # If already raising TimeoutExceeded, let it propagate
        return False

    def _trigger(self):
        self._timed_out = True


class _TimeoutTimer(threading.Thread):
    """Internal daemon thread that triggers a timeout context manager."""

    def __init__(self, seconds: float, ctx: timeout):
        super().__init__(daemon=True)
        self.seconds = seconds
        self.ctx = ctx
        self._cancel_event = threading.Event()

    def run(self):
        self._cancel_event.wait(timeout=self.seconds)
        if not self._cancel_event.is_set():
            self.ctx._trigger()

    def cancel(self):
        self._cancel_event.set()


# Note: The context manager approach with threads has a fundamental limitation —
# we can't interrupt blocking Python code from another thread.
# For the context manager, we use with_timeout internally via a wrapper.
# Redefine to use the reliable thread-join approach:


class timeout:
    """
    Context manager for timeouts.

    Example::

        with timeout(30):
            result = call_llm(messages)

    Raises:
        TimeoutExceeded: If the block does not complete within the given seconds.

    Note: Uses threading internally; the block runs in a new thread.
    Wrap synchronous blocking calls (LLM API, HTTP) — this is the primary use case.
    """

    def __init__(self, seconds: float):
        self.seconds = seconds
        self._result = None
        self._exception = None
        self._completed = False
        self._start = None

    def __enter__(self):
        self._start = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # The context manager is a lightweight wrapper.
        # For timeout enforcement, use with_timeout() or timeout_decorator().
        # The context manager tracks entry time for elapsed reporting.
        return False

    def _run_with_timeout(self, func, *args, **kwargs):
        """Helper to run a function within this timeout context."""
        remaining = self.seconds - (time.monotonic() - self._start)
        if remaining <= 0:
            raise TimeoutExceeded(self.seconds, time.monotonic() - self._start)
        return with_timeout(remaining, func, *args, **kwargs)


# Simpler, more useful context manager that actually enforces timeouts
# by running the body in a thread. However, Python context managers don't
# "inject" into the body. The standard approach is to use it with a callable.
# For a true blocking context manager, we need a different pattern.
#
# The most correct cross-platform approach for a context manager is
# to use it with with_timeout for the inner call, OR to implement
# via threading.Event and have the context manager interrupt via a flag.
#
# We provide both patterns:
# 1. with_timeout(seconds, func) — wraps a callable (most reliable)
# 2. timeout context manager — best effort, raises on __exit__ if elapsed
#
# For LLM calls the recommended pattern is with_timeout() or timeout_decorator().


class timeout:
    """
    Context manager / timer for deadline tracking.

    For reliable timeout enforcement, prefer with_timeout() or @timeout_decorator.

    This context manager raises TimeoutExceeded in __exit__ if the block took
    longer than the deadline — useful for detecting slow operations after the fact,
    or combined with with_timeout internally.

    Example with a callable (recommended for hard enforcement)::

        with timeout(30) as t:
            result = t.run(call_llm, messages)

    Example as elapsed checker (soft enforcement)::

        with timeout(30):
            result = call_llm(messages)
        # raises TimeoutExceeded on exit if call_llm took too long
    """

    def __init__(self, seconds: float):
        self.seconds = seconds
        self._start = None

    def __enter__(self):
        self._start = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.monotonic() - self._start
        if exc_type is None and elapsed > self.seconds:
            raise TimeoutExceeded(self.seconds, elapsed)
        return False

    def run(self, func, *args, **kwargs):
        """Run func with the remaining timeout from this context."""
        remaining = self.seconds - (time.monotonic() - self._start)
        if remaining <= 0:
            elapsed = time.monotonic() - self._start
            raise TimeoutExceeded(self.seconds, elapsed)
        return with_timeout(remaining, func, *args, **kwargs)


def timeout_decorator(seconds: float):
    """
    Decorator for timeout enforcement.

    Example::

        @timeout_decorator(30)
        def call_llm(messages):
            ...

    Args:
        seconds: Maximum seconds the function may run.

    Returns:
        Decorator that wraps the function with timeout enforcement.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return with_timeout(seconds, func, *args, **kwargs)

        return wrapper

    return decorator


async def with_timeout_async(seconds: float, coro):
    """
    Run an async coroutine with a timeout.
    Uses asyncio.wait_for internally.
    Raises TimeoutExceeded (not asyncio.TimeoutError).

    Args:
        seconds: Maximum seconds to wait.
        coro: Awaitable coroutine.

    Returns:
        Return value of the coroutine.

    Raises:
        TimeoutExceeded: If the coroutine does not complete within seconds.
        Exception: Any exception from the coroutine is re-raised.
    """
    start = time.monotonic()
    try:
        return await asyncio.wait_for(coro, timeout=seconds)
    except asyncio.TimeoutError:
        elapsed = time.monotonic() - start
        raise TimeoutExceeded(seconds, elapsed)


def timeout_async(seconds: float):
    """
    Decorator for async timeout enforcement.

    Example::

        @timeout_async(30)
        async def call_llm_async(messages):
            ...

    Args:
        seconds: Maximum seconds the async function may run.

    Returns:
        Decorator that wraps the async function with timeout enforcement.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await with_timeout_async(seconds, func(*args, **kwargs))

        return wrapper

    return decorator
