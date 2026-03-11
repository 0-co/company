"""Tests for export functionality (JSONL, get_spans, get_trace_tree)."""

import json
import os
import tempfile
import unittest

from agent_trace.tracer import Tracer
from agent_trace.export import spans_to_jsonl, write_jsonl, read_jsonl


class TestExportJsonl(unittest.TestCase):
    def test_export_jsonl_creates_file(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            pass
        with tempfile.NamedTemporaryFile(mode="r", suffix=".jsonl", delete=False) as fh:
            path = fh.name
        try:
            tracer.export_jsonl(path)
            self.assertTrue(os.path.exists(path))
        finally:
            os.unlink(path)

    def test_export_jsonl_writes_valid_json_lines(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            pass
        with tempfile.NamedTemporaryFile(mode="r", suffix=".jsonl", delete=False) as fh:
            path = fh.name
        try:
            tracer.export_jsonl(path)
            with open(path) as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        obj = json.loads(line)
                        self.assertIsInstance(obj, dict)
        finally:
            os.unlink(path)

    def test_each_line_is_a_span_dict(self):
        tracer = Tracer()
        with tracer.start_span("first"):
            pass
        with tracer.start_span("second"):
            pass
        with tempfile.NamedTemporaryFile(mode="r", suffix=".jsonl", delete=False) as fh:
            path = fh.name
        try:
            tracer.export_jsonl(path)
            with open(path) as fh:
                lines = [l.strip() for l in fh if l.strip()]
            self.assertEqual(len(lines), 2)
            names = [json.loads(l)["name"] for l in lines]
            self.assertIn("first", names)
            self.assertIn("second", names)
        finally:
            os.unlink(path)

    def test_export_appends_to_existing_file(self):
        tracer1 = Tracer()
        with tracer1.start_span("run1"):
            pass

        tracer2 = Tracer()
        with tracer2.start_span("run2"):
            pass

        with tempfile.NamedTemporaryFile(mode="r", suffix=".jsonl", delete=False) as fh:
            path = fh.name
        try:
            tracer1.export_jsonl(path)
            tracer2.export_jsonl(path)
            with open(path) as fh:
                lines = [l.strip() for l in fh if l.strip()]
            self.assertEqual(len(lines), 2)
        finally:
            os.unlink(path)

    def test_all_span_fields_present_in_export(self):
        tracer = Tracer()
        with tracer.start_span("op") as span:
            span.set_attribute("k", "v")
        with tempfile.NamedTemporaryFile(mode="r", suffix=".jsonl", delete=False) as fh:
            path = fh.name
        try:
            tracer.export_jsonl(path)
            with open(path) as fh:
                data = json.loads(fh.readline())
            for field in ["span_id", "trace_id", "name", "start_time", "end_time",
                          "attributes", "events", "status", "error_message"]:
                self.assertIn(field, data)
        finally:
            os.unlink(path)


class TestGetSpans(unittest.TestCase):
    def test_get_spans_returns_list_of_dicts(self):
        tracer = Tracer()
        with tracer.start_span("op"):
            pass
        spans = tracer.get_spans()
        self.assertIsInstance(spans, list)
        self.assertIsInstance(spans[0], dict)

    def test_empty_tracer_returns_empty_list(self):
        tracer = Tracer()
        self.assertEqual(tracer.get_spans(), [])

    def test_get_spans_count_matches_completed_spans(self):
        tracer = Tracer()
        for name in ["a", "b", "c"]:
            with tracer.start_span(name):
                pass
        self.assertEqual(len(tracer.get_spans()), 3)


class TestGetTraceTree(unittest.TestCase):
    def test_trace_tree_root_has_name(self):
        tracer = Tracer()
        with tracer.start_span("root"):
            pass
        tree = tracer.get_trace_tree()
        self.assertEqual(tree["name"], "root")

    def test_trace_tree_correctly_nests_parent_child(self):
        tracer = Tracer()
        with tracer.start_span("parent"):
            with tracer.start_span("child"):
                pass
        tree = tracer.get_trace_tree()
        self.assertEqual(tree["name"], "parent")
        self.assertEqual(len(tree["children"]), 1)
        self.assertEqual(tree["children"][0]["name"], "child")

    def test_empty_tracer_tree_has_empty_children(self):
        tracer = Tracer()
        tree = tracer.get_trace_tree()
        self.assertEqual(tree["children"], [])

    def test_multiple_children_all_appear(self):
        tracer = Tracer()
        with tracer.start_span("root"):
            with tracer.start_span("c1"):
                pass
            with tracer.start_span("c2"):
                pass
        tree = tracer.get_trace_tree()
        child_names = [c["name"] for c in tree["children"]]
        self.assertIn("c1", child_names)
        self.assertIn("c2", child_names)


class TestExportHelpers(unittest.TestCase):
    def test_spans_to_jsonl_returns_string(self):
        spans = [{"span_id": "abc", "name": "op"}]
        result = spans_to_jsonl(spans)
        self.assertIsInstance(result, str)
        self.assertIn('"name": "op"', result)

    def test_write_and_read_jsonl_roundtrip(self):
        spans = [
            {"span_id": "aaa", "name": "first"},
            {"span_id": "bbb", "name": "second"},
        ]
        with tempfile.NamedTemporaryFile(mode="r", suffix=".jsonl", delete=False) as fh:
            path = fh.name
        try:
            write_jsonl(path, spans, append=False)
            loaded = read_jsonl(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0]["name"], "first")
            self.assertEqual(loaded[1]["name"], "second")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
