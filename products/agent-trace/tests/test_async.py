"""Tests for async span support and the trace_span decorator."""

import asyncio
import time
import unittest

from agent_trace import Tracer, trace_span, get_current_span


class TestTraceSpanDecorator(unittest.TestCase):
    """Tests for the @trace_span decorator (sync + async)."""

    def test_decorator_bare_on_sync_function(self):
        """@trace_span without parentheses on a sync function."""
        tracer = Tracer()

        @trace_span
        def my_fn():
            return 42

        with tracer.start_span("root"):
            result = my_fn()
        self.assertEqual(result, 42)

    def test_decorator_with_name_on_sync_function(self):
        @trace_span("custom_op")
        def my_fn():
            return "hello"

        result = my_fn()
        self.assertEqual(result, "hello")

    def test_sync_decorator_records_span(self):
        tracer = Tracer()

        @trace_span("recorded_op")
        def inner():
            pass

        with tracer.start_span("root"):
            inner()

        # The inner span should be recorded in whatever tracer was active.
        spans = tracer.get_spans()
        names = [s["name"] for s in spans]
        self.assertIn("recorded_op", names)

    def test_decorator_preserves_function_name(self):
        @trace_span
        def original_name():
            pass

        self.assertEqual(original_name.__name__, "original_name")

    def test_decorator_preserves_function_name_with_explicit_span_name(self):
        @trace_span("different_span_name")
        def my_function():
            pass

        self.assertEqual(my_function.__name__, "my_function")

    def test_sync_decorator_exception_propagates(self):
        @trace_span("risky")
        def risky():
            raise RuntimeError("failure")

        with self.assertRaises(RuntimeError):
            risky()


class TestAsyncDecorator(unittest.IsolatedAsyncioTestCase):
    async def test_decorator_on_async_function(self):
        @trace_span("async_op")
        async def my_async():
            return "done"

        result = await my_async()
        self.assertEqual(result, "done")

    async def test_async_span_records_timing(self):
        tracer = Tracer()

        @trace_span("timed_async")
        async def slow():
            await asyncio.sleep(0.01)

        with tracer.start_span("root"):
            await slow()

        spans = tracer.get_spans()
        timed = next((s for s in spans if s["name"] == "timed_async"), None)
        self.assertIsNotNone(timed)
        self.assertGreaterEqual(timed["end_time"] - timed["start_time"], 0.0)

    async def test_async_decorator_with_explicit_name(self):
        @trace_span("explicit_async_name")
        async def unnamed():
            return 1

        result = await unnamed()
        self.assertEqual(result, 1)

    async def test_nested_async_spans_have_parent_child(self):
        tracer = Tracer()

        async def child():
            with tracer.start_span("child_span") as span:
                return span.span_id

        with tracer.start_span("parent_span") as parent:
            child_id = await child()

        spans = {s["name"]: s for s in tracer.get_spans()}
        self.assertEqual(spans["child_span"]["parent_span_id"], parent.span_id)

    async def test_async_context_manager_sets_end_time(self):
        tracer = Tracer()
        with tracer.start_span("async_cm") as span:
            await asyncio.sleep(0)

        spans = tracer.get_spans()
        self.assertIsNotNone(spans[0]["end_time"])

    async def test_async_error_recording(self):
        tracer = Tracer()

        with tracer.start_span("fallible") as span:
            try:
                raise ValueError("async failure")
            except ValueError as exc:
                span.record_error(exc)

        spans = tracer.get_spans()
        self.assertEqual(spans[0]["status"], "error")
        self.assertEqual(spans[0]["error_message"], "async failure")

    async def test_concurrent_async_spans_dont_interfere(self):
        """asyncio.gather with two independent tracers."""
        results = {}

        async def task(name: str) -> None:
            tracer = Tracer()
            with tracer.start_span(f"{name}_span") as span:
                await asyncio.sleep(0.01)
                results[name] = span.span_id

        await asyncio.gather(task("task_a"), task("task_b"))

        self.assertIn("task_a", results)
        self.assertIn("task_b", results)
        self.assertNotEqual(results["task_a"], results["task_b"])

    async def test_async_decorator_exception_propagates(self):
        @trace_span("async_risky")
        async def risky():
            raise RuntimeError("async boom")

        with self.assertRaises(RuntimeError):
            await risky()

    async def test_async_span_status_error_on_exception(self):
        tracer = Tracer()

        try:
            with tracer.start_span("failing_async") as span:
                raise ValueError("crash")
        except ValueError:
            pass

        spans = tracer.get_spans()
        self.assertEqual(spans[0]["status"], "error")


if __name__ == "__main__":
    unittest.main()
