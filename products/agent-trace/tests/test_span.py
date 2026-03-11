"""Tests for agent_trace.span.Span."""

import json
import time
import unittest

from agent_trace.span import Span


def _make_span(**kwargs) -> Span:
    defaults = {"name": "test_op", "trace_id": "abcdef1234567890"}
    defaults.update(kwargs)
    return Span(**defaults)


class TestSpanIdentity(unittest.TestCase):
    def test_span_has_span_id(self):
        span = _make_span()
        self.assertIsNotNone(span.span_id)
        self.assertIsInstance(span.span_id, str)

    def test_span_id_is_8_chars(self):
        span = _make_span()
        self.assertEqual(len(span.span_id), 8)

    def test_two_spans_have_different_ids(self):
        a = _make_span()
        b = _make_span()
        self.assertNotEqual(a.span_id, b.span_id)

    def test_span_stores_trace_id(self):
        span = _make_span(trace_id="deadbeef01234567")
        self.assertEqual(span.trace_id, "deadbeef01234567")

    def test_span_without_parent_has_none_parent_span_id(self):
        span = _make_span()
        self.assertIsNone(span.parent_span_id)

    def test_span_with_parent_stores_parent_span_id(self):
        span = _make_span(parent_span_id="aabbccdd")
        self.assertEqual(span.parent_span_id, "aabbccdd")


class TestSpanTiming(unittest.TestCase):
    def test_span_records_start_time(self):
        before = time.time()
        span = _make_span()
        after = time.time()
        self.assertGreaterEqual(span.start_time, before)
        self.assertLessEqual(span.start_time, after)

    def test_end_time_is_none_before_exit(self):
        span = _make_span()
        self.assertIsNone(span.end_time)

    def test_context_manager_sets_end_time(self):
        span = _make_span()
        with span:
            pass
        self.assertIsNotNone(span.end_time)
        self.assertGreaterEqual(span.end_time, span.start_time)

    def test_context_manager_returns_self(self):
        span = _make_span()
        with span as s:
            self.assertIs(s, span)


class TestSpanAttributes(unittest.TestCase):
    def test_set_attribute_stores_value(self):
        span = _make_span()
        span.set_attribute("model", "claude-sonnet-4-6")
        self.assertEqual(span.attributes["model"], "claude-sonnet-4-6")

    def test_multiple_attributes_can_be_set(self):
        span = _make_span()
        span.set_attribute("tokens", 1234)
        span.set_attribute("cost", 0.005)
        self.assertEqual(span.attributes["tokens"], 1234)
        self.assertEqual(span.attributes["cost"], 0.005)

    def test_attribute_overwrites_previous(self):
        span = _make_span()
        span.set_attribute("x", 1)
        span.set_attribute("x", 2)
        self.assertEqual(span.attributes["x"], 2)


class TestSpanEvents(unittest.TestCase):
    def test_add_event_stores_event(self):
        span = _make_span()
        span.add_event("tool_call", {"tool": "search"})
        self.assertEqual(len(span.events), 1)
        self.assertEqual(span.events[0]["name"], "tool_call")

    def test_event_has_timestamp(self):
        before = time.time()
        span = _make_span()
        span.add_event("tick")
        after = time.time()
        ts = span.events[0]["timestamp"]
        self.assertGreaterEqual(ts, before)
        self.assertLessEqual(ts, after)

    def test_event_without_attributes_defaults_to_empty_dict(self):
        span = _make_span()
        span.add_event("ping")
        self.assertEqual(span.events[0]["attributes"], {})

    def test_multiple_events_stored_in_order(self):
        span = _make_span()
        span.add_event("first")
        span.add_event("second")
        self.assertEqual(span.events[0]["name"], "first")
        self.assertEqual(span.events[1]["name"], "second")


class TestSpanError(unittest.TestCase):
    def test_record_error_sets_status_to_error(self):
        span = _make_span()
        span.record_error(ValueError("bad input"))
        self.assertEqual(span.status, "error")

    def test_record_error_stores_message(self):
        span = _make_span()
        span.record_error(ValueError("bad input"))
        self.assertEqual(span.error_message, "bad input")

    def test_record_error_adds_event_with_exception_type(self):
        span = _make_span()
        span.record_error(RuntimeError("boom"))
        error_events = [e for e in span.events if e["name"] == "error"]
        self.assertEqual(len(error_events), 1)
        self.assertEqual(error_events[0]["attributes"]["exception.type"], "RuntimeError")

    def test_default_status_is_ok(self):
        span = _make_span()
        self.assertEqual(span.status, "ok")

    def test_exception_in_context_manager_sets_status_error(self):
        span = _make_span()
        try:
            with span:
                raise ValueError("oops")
        except ValueError:
            pass
        self.assertEqual(span.status, "error")


class TestSpanSerialization(unittest.TestCase):
    def test_to_dict_is_json_serializable(self):
        span = _make_span()
        span.set_attribute("model", "claude")
        span.add_event("tick", {"k": "v"})
        with span:
            pass
        data = span.to_dict()
        # Should not raise.
        json_str = json.dumps(data)
        self.assertIn("span_id", json_str)

    def test_to_dict_contains_all_required_fields(self):
        span = _make_span()
        with span:
            pass
        data = span.to_dict()
        required = [
            "span_id", "trace_id", "parent_span_id", "name",
            "start_time", "end_time", "attributes", "events",
            "status", "error_message",
        ]
        for field in required:
            self.assertIn(field, data, f"Missing field: {field}")


if __name__ == "__main__":
    unittest.main()
