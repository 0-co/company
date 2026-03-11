"""
Tests for agent_timeout.timeout module.
"""

import asyncio
import time
import unittest

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_timeout import (
    TimeoutExceeded,
    timeout,
    timeout_async,
    timeout_decorator,
    with_timeout,
    with_timeout_async,
)


def fast_func(x=1):
    return x * 2


def slow_func(duration=5.0):
    time.sleep(duration)
    return "done"


def raises_func():
    raise ValueError("something went wrong")


def kwargs_func(a, b, multiplier=1):
    return (a + b) * multiplier


async def fast_coro(x=1):
    await asyncio.sleep(0.01)
    return x * 3


async def slow_coro(duration=5.0):
    await asyncio.sleep(duration)
    return "async done"


async def raises_coro():
    raise RuntimeError("async error")


class TestWithTimeout(unittest.TestCase):
    """Tests for with_timeout()."""

    def test_fast_function_completes_normally(self):
        result = with_timeout(5.0, fast_func, 10)
        self.assertEqual(result, 20)

    def test_slow_function_raises_timeout_exceeded(self):
        with self.assertRaises(TimeoutExceeded):
            with_timeout(0.1, slow_func, 5.0)

    def test_exception_propagates_not_timeout(self):
        with self.assertRaises(ValueError) as ctx:
            with_timeout(5.0, raises_func)
        self.assertEqual(str(ctx.exception), "something went wrong")

    def test_timeout_zero_raises_timeout_exceeded(self):
        with self.assertRaises(TimeoutExceeded):
            with_timeout(0.0, fast_func, 1)

    def test_returns_correct_value(self):
        result = with_timeout(5.0, fast_func, 7)
        self.assertEqual(result, 14)

    def test_kwargs_pass_through_correctly(self):
        result = with_timeout(5.0, kwargs_func, 3, 4, multiplier=2)
        self.assertEqual(result, 14)  # (3 + 4) * 2

    def test_timeout_exceeded_has_seconds_attribute(self):
        try:
            with_timeout(0.05, slow_func, 5.0)
            self.fail("Expected TimeoutExceeded")
        except TimeoutExceeded as e:
            self.assertEqual(e.seconds, 0.05)

    def test_timeout_exceeded_has_elapsed_attribute(self):
        try:
            with_timeout(0.05, slow_func, 5.0)
            self.fail("Expected TimeoutExceeded")
        except TimeoutExceeded as e:
            self.assertGreaterEqual(e.elapsed, 0.05)

    def test_large_timeout_does_not_slow_fast_functions(self):
        start = time.monotonic()
        result = with_timeout(30.0, fast_func, 5)
        elapsed = time.monotonic() - start
        self.assertEqual(result, 10)
        # Fast function should complete in well under 1 second even with large timeout
        self.assertLess(elapsed, 1.0)

    def test_no_args_function(self):
        def no_args():
            return 42

        result = with_timeout(5.0, no_args)
        self.assertEqual(result, 42)

    def test_returns_none_when_function_returns_none(self):
        def returns_none():
            return None

        result = with_timeout(5.0, returns_none)
        self.assertIsNone(result)

    def test_exception_type_preserved(self):
        def raises_type_error():
            raise TypeError("type error")

        with self.assertRaises(TypeError):
            with_timeout(5.0, raises_type_error)


class TestTimeoutContextManager(unittest.TestCase):
    """Tests for timeout context manager."""

    def test_fast_code_completes(self):
        start = time.monotonic()
        with timeout(5.0) as t:
            result = t.run(fast_func, 3)
        self.assertEqual(result, 6)

    def test_slow_code_raises_timeout_exceeded(self):
        with self.assertRaises(TimeoutExceeded):
            with timeout(0.1) as t:
                t.run(slow_func, 5.0)

    def test_context_manager_exposes_run_method(self):
        with timeout(5.0) as t:
            self.assertTrue(hasattr(t, "run"))

    def test_context_manager_elapsed_check(self):
        """Context manager raises TimeoutExceeded on exit if block was too slow."""
        with self.assertRaises(TimeoutExceeded):
            with timeout(0.01):
                time.sleep(0.1)

    def test_context_manager_fast_exits_cleanly(self):
        """Fast block inside context manager does not raise."""
        with timeout(5.0):
            x = 1 + 1
        self.assertEqual(x, 2)

    def test_context_manager_run_raises_on_exhausted(self):
        """t.run() raises BudgetExhausted-style TimeoutExceeded if no time left."""
        with self.assertRaises(TimeoutExceeded):
            with timeout(0.05) as t:
                time.sleep(0.1)
                t.run(fast_func)  # no time left


class TestTimeoutDecorator(unittest.TestCase):
    """Tests for timeout_decorator."""

    def test_fast_function_passes(self):
        @timeout_decorator(5.0)
        def add(a, b):
            return a + b

        result = add(3, 4)
        self.assertEqual(result, 7)

    def test_slow_function_raises(self):
        @timeout_decorator(0.1)
        def slow():
            time.sleep(5.0)
            return "done"

        with self.assertRaises(TimeoutExceeded):
            slow()

    def test_preserves_function_name(self):
        @timeout_decorator(5.0)
        def my_special_function():
            return 1

        self.assertEqual(my_special_function.__name__, "my_special_function")

    def test_preserves_function_docstring(self):
        @timeout_decorator(5.0)
        def documented():
            """This is a docstring."""
            return 1

        self.assertEqual(documented.__doc__, "This is a docstring.")

    def test_kwargs_pass_through(self):
        @timeout_decorator(5.0)
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}"

        result = greet("World", greeting="Hi")
        self.assertEqual(result, "Hi, World")

    def test_exception_propagates(self):
        @timeout_decorator(5.0)
        def failing():
            raise KeyError("missing key")

        with self.assertRaises(KeyError):
            failing()


class TestWithTimeoutAsync(unittest.TestCase):
    """Tests for with_timeout_async."""

    def test_fast_coroutine_returns_value(self):
        result = asyncio.run(with_timeout_async(5.0, fast_coro(10)))
        self.assertEqual(result, 30)

    def test_slow_coroutine_raises_timeout_exceeded(self):
        with self.assertRaises(TimeoutExceeded):
            asyncio.run(with_timeout_async(0.05, slow_coro(5.0)))

    def test_raises_timeout_exceeded_not_asyncio_timeout_error(self):
        """Must raise TimeoutExceeded, not asyncio.TimeoutError."""
        try:
            asyncio.run(with_timeout_async(0.05, slow_coro(5.0)))
            self.fail("Expected TimeoutExceeded")
        except TimeoutExceeded:
            pass
        except asyncio.TimeoutError:
            self.fail("Should not raise asyncio.TimeoutError, expected TimeoutExceeded")

    def test_async_exception_propagates(self):
        with self.assertRaises(RuntimeError) as ctx:
            asyncio.run(with_timeout_async(5.0, raises_coro()))
        self.assertEqual(str(ctx.exception), "async error")

    def test_async_timeout_exceeded_has_attributes(self):
        try:
            asyncio.run(with_timeout_async(0.05, slow_coro(5.0)))
            self.fail("Expected TimeoutExceeded")
        except TimeoutExceeded as e:
            self.assertEqual(e.seconds, 0.05)
            self.assertGreaterEqual(e.elapsed, 0.05)


class TestTimeoutAsyncDecorator(unittest.TestCase):
    """Tests for timeout_async decorator."""

    def test_fast_async_function_passes(self):
        @timeout_async(5.0)
        async def add_async(a, b):
            await asyncio.sleep(0.01)
            return a + b

        result = asyncio.run(add_async(3, 4))
        self.assertEqual(result, 7)

    def test_slow_async_function_raises(self):
        @timeout_async(0.05)
        async def slow_async():
            await asyncio.sleep(5.0)
            return "done"

        with self.assertRaises(TimeoutExceeded):
            asyncio.run(slow_async())

    def test_async_decorator_preserves_name(self):
        @timeout_async(5.0)
        async def my_async_function():
            return 1

        self.assertEqual(my_async_function.__name__, "my_async_function")

    def test_async_decorator_raises_timeout_exceeded_not_asyncio(self):
        @timeout_async(0.05)
        async def slow_async():
            await asyncio.sleep(5.0)

        try:
            asyncio.run(slow_async())
            self.fail("Expected TimeoutExceeded")
        except TimeoutExceeded:
            pass
        except asyncio.TimeoutError:
            self.fail("Should be TimeoutExceeded not asyncio.TimeoutError")


class TestTimeoutExceededAttributes(unittest.TestCase):
    """Tests for TimeoutExceeded exception attributes."""

    def test_has_seconds_attribute(self):
        exc = TimeoutExceeded(seconds=10.0, elapsed=10.5)
        self.assertEqual(exc.seconds, 10.0)

    def test_has_elapsed_attribute(self):
        exc = TimeoutExceeded(seconds=10.0, elapsed=10.5)
        self.assertEqual(exc.elapsed, 10.5)

    def test_message_contains_elapsed(self):
        exc = TimeoutExceeded(seconds=10.0, elapsed=10.5)
        self.assertIn("10.5", str(exc))

    def test_message_contains_limit(self):
        exc = TimeoutExceeded(seconds=10.0, elapsed=10.5)
        self.assertIn("10.0", str(exc))

    def test_is_exception(self):
        exc = TimeoutExceeded(seconds=5.0, elapsed=6.0)
        self.assertIsInstance(exc, Exception)


if __name__ == "__main__":
    unittest.main()
