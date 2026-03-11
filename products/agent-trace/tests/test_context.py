"""Tests for agent_trace.context module-level functions."""

import threading
import unittest

from agent_trace.context import get_current_span, get_current_tracer
from agent_trace.tracer import Tracer


class TestGetCurrentSpan(unittest.TestCase):
    def test_returns_none_outside_span(self):
        self.assertIsNone(get_current_span())

    def test_returns_span_inside_context_manager(self):
        tracer = Tracer()
        with tracer.start_span("op") as span:
            current = get_current_span()
            self.assertIs(current, span)

    def test_returns_inner_span_in_nested_context(self):
        tracer = Tracer()
        with tracer.start_span("outer"):
            with tracer.start_span("inner") as inner:
                current = get_current_span()
                self.assertIs(current, inner)

    def test_returns_outer_span_after_inner_exits(self):
        tracer = Tracer()
        with tracer.start_span("outer") as outer:
            with tracer.start_span("inner"):
                pass
            current = get_current_span()
            self.assertIs(current, outer)

    def test_returns_none_after_all_spans_exit(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            pass
        self.assertIsNone(get_current_span())

    def test_exception_does_not_leave_span_on_stack(self):
        tracer = Tracer()
        try:
            with tracer.start_span("op"):
                raise ValueError("boom")
        except ValueError:
            pass
        self.assertIsNone(get_current_span())


class TestGetCurrentTracer(unittest.TestCase):
    def test_returns_none_outside_span(self):
        self.assertIsNone(get_current_tracer())

    def test_returns_tracer_inside_span(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            current = get_current_tracer()
            self.assertIs(current, tracer)

    def test_returns_none_after_span_exits(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            pass
        self.assertIsNone(get_current_tracer())

    def test_returns_most_recent_tracer_in_nested_context(self):
        outer_tracer = Tracer()
        inner_tracer = Tracer()
        with outer_tracer.start_span("outer"):
            with inner_tracer.start_span("inner"):
                current = get_current_tracer()
                self.assertIs(current, inner_tracer)
            current_after_inner = get_current_tracer()
            self.assertIs(current_after_inner, outer_tracer)


class TestThreadIsolation(unittest.TestCase):
    def test_span_from_thread_a_not_visible_in_thread_b(self):
        """Thread B's get_current_span should be None while thread A has an active span."""
        barrier = threading.Barrier(2)
        seen_in_b: dict = {}

        def thread_a() -> None:
            tracer = Tracer()
            with tracer.start_span("thread_a_span"):
                barrier.wait()  # Wait for thread B to check
                barrier.wait()  # Hold span open while B checks

        def thread_b() -> None:
            barrier.wait()  # Wait until A has entered its span
            seen_in_b["span"] = get_current_span()
            barrier.wait()

        ta = threading.Thread(target=thread_a)
        tb = threading.Thread(target=thread_b)
        ta.start()
        tb.start()
        ta.join()
        tb.join()

        self.assertIsNone(seen_in_b["span"])

    def test_each_thread_has_own_span_stack(self):
        results = {}

        def worker(name: str) -> None:
            tracer = Tracer()
            with tracer.start_span(f"{name}_span") as span:
                # Use span_id (a random hex string) instead of id() to avoid
                # address reuse after garbage collection.
                results[name] = span.span_id

        threads = [threading.Thread(target=worker, args=(f"t{i}",)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Each thread should have been inside a different span.
        span_ids = list(results.values())
        self.assertEqual(len(set(span_ids)), 3)


if __name__ == "__main__":
    unittest.main()
