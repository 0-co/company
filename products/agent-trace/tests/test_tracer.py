"""Tests for agent_trace.tracer.Tracer."""

import threading
import time
import unittest

from agent_trace.tracer import Tracer
from agent_trace.context import get_current_span


class TestTracerInit(unittest.TestCase):
    def test_tracer_generates_trace_id(self):
        tracer = Tracer()
        self.assertIsNotNone(tracer.trace_id)
        self.assertIsInstance(tracer.trace_id, str)

    def test_trace_id_is_16_chars(self):
        tracer = Tracer()
        self.assertEqual(len(tracer.trace_id), 16)

    def test_tracer_with_explicit_trace_id_uses_it(self):
        tracer = Tracer(trace_id="abcdef1234567890")
        self.assertEqual(tracer.trace_id, "abcdef1234567890")

    def test_two_tracers_have_different_trace_ids(self):
        a = Tracer()
        b = Tracer()
        self.assertNotEqual(a.trace_id, b.trace_id)


class TestSpanCreation(unittest.TestCase):
    def test_start_span_returns_context_manager(self):
        tracer = Tracer()
        cm = tracer.start_span("op")
        with cm as span:
            self.assertEqual(span.name, "op")
            self.assertEqual(span.trace_id, tracer.trace_id)

    def test_span_has_correct_trace_id(self):
        tracer = Tracer(trace_id="deadbeef01234567")
        with tracer.start_span("op") as span:
            self.assertEqual(span.trace_id, "deadbeef01234567")

    def test_span_without_nesting_has_no_parent(self):
        tracer = Tracer()
        with tracer.start_span("root") as span:
            self.assertIsNone(span.parent_span_id)


class TestParentChildRelationship(unittest.TestCase):
    def test_nested_spans_have_correct_parent_child(self):
        tracer = Tracer()
        with tracer.start_span("outer") as outer:
            outer_id = outer.span_id
            with tracer.start_span("inner") as inner:
                self.assertEqual(inner.parent_span_id, outer_id)

    def test_two_sequential_children_both_point_to_parent(self):
        tracer = Tracer()
        with tracer.start_span("root") as root:
            root_id = root.span_id
            with tracer.start_span("child_a") as child_a:
                a_parent = child_a.parent_span_id
            with tracer.start_span("child_b") as child_b:
                b_parent = child_b.parent_span_id
        self.assertEqual(a_parent, root_id)
        self.assertEqual(b_parent, root_id)

    def test_manual_parent_span_id_overrides_auto(self):
        tracer = Tracer()
        with tracer.start_span("root") as root:
            with tracer.start_span("inner", parent_span_id="explicit00") as inner:
                self.assertEqual(inner.parent_span_id, "explicit00")

    def test_three_levels_deep(self):
        tracer = Tracer()
        with tracer.start_span("l1") as l1:
            with tracer.start_span("l2") as l2:
                with tracer.start_span("l3") as l3:
                    self.assertEqual(l3.parent_span_id, l2.span_id)
                    self.assertEqual(l2.parent_span_id, l1.span_id)


class TestSpanCollection(unittest.TestCase):
    def test_completed_span_appears_in_get_spans(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            pass
        spans = tracer.get_spans()
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0]["name"], "op")

    def test_active_span_not_in_get_spans(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            self.assertEqual(len(tracer.get_spans()), 0)

    def test_multiple_spans_all_collected(self):
        tracer = Tracer()
        with tracer.start_span("a"):
            pass
        with tracer.start_span("b"):
            pass
        self.assertEqual(len(tracer.get_spans()), 2)

    def test_get_spans_returns_dicts(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            pass
        spans = tracer.get_spans()
        self.assertIsInstance(spans[0], dict)


class TestContext(unittest.TestCase):
    def test_get_context_returns_trace_id(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            ctx = tracer.get_context()
        self.assertEqual(ctx["trace_id"], tracer.trace_id)

    def test_get_context_returns_current_span_id(self):
        tracer = Tracer()
        with tracer.start_span("op") as span:
            ctx = tracer.get_context()
            self.assertEqual(ctx["span_id"], span.span_id)

    def test_from_context_uses_same_trace_id(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            ctx = tracer.get_context()
        child_tracer = Tracer.from_context(ctx)
        self.assertEqual(child_tracer.trace_id, tracer.trace_id)

    def test_span_from_context_has_remote_parent(self):
        tracer = Tracer()
        with tracer.start_span("root") as root:
            ctx = tracer.get_context()
        child_tracer = Tracer.from_context(ctx)
        with child_tracer.start_span("remote_op") as remote_span:
            self.assertEqual(remote_span.parent_span_id, root.span_id)


class TestTraceTree(unittest.TestCase):
    def test_get_trace_tree_returns_dict(self):
        tracer = Tracer()
        with tracer.start_span("root"):
            pass
        tree = tracer.get_trace_tree()
        self.assertIsInstance(tree, dict)

    def test_tree_root_has_children_key(self):
        tracer = Tracer()
        with tracer.start_span("root"):
            pass
        tree = tracer.get_trace_tree()
        self.assertIn("children", tree)

    def test_tree_nests_child_under_parent(self):
        tracer = Tracer()
        with tracer.start_span("root"):
            with tracer.start_span("child"):
                pass
        tree = tracer.get_trace_tree()
        self.assertEqual(tree["name"], "root")
        self.assertEqual(len(tree["children"]), 1)
        self.assertEqual(tree["children"][0]["name"], "child")

    def test_empty_tracer_returns_wrapper_with_empty_children(self):
        tracer = Tracer()
        tree = tracer.get_trace_tree()
        self.assertIn("children", tree)
        self.assertEqual(len(tree["children"]), 0)


class TestThreadIsolation(unittest.TestCase):
    def test_concurrent_spans_use_own_stack(self):
        """Two threads each build their own span hierarchy."""
        results = {}

        def thread_work(thread_name: str) -> None:
            tracer = Tracer()
            with tracer.start_span(f"{thread_name}_outer") as outer:
                with tracer.start_span(f"{thread_name}_inner") as inner:
                    results[thread_name] = {
                        "inner_parent": inner.parent_span_id,
                        "outer_id": outer.span_id,
                    }

        t1 = threading.Thread(target=thread_work, args=("thread_a",))
        t2 = threading.Thread(target=thread_work, args=("thread_b",))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(results["thread_a"]["inner_parent"], results["thread_a"]["outer_id"])
        self.assertEqual(results["thread_b"]["inner_parent"], results["thread_b"]["outer_id"])
        # Each thread's outer span ID is different.
        self.assertNotEqual(results["thread_a"]["outer_id"], results["thread_b"]["outer_id"])


if __name__ == "__main__":
    unittest.main()
