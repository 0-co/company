"""
Tests for agent-log.

Run with:
    python -m pytest tests/
or:
    python tests/test_agent_log.py
"""

import io
import json
import sys
import time
import unittest
from unittest.mock import patch

# Allow running from repo root or from products/agent-log/
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_log import AgentLogger
from agent_log.redactor import redact_string, redact_dict, redact_value
from agent_log.span import TOKEN_COSTS, _calculate_cost


def _capture_jsonl(logger_name: str, **logger_kwargs):
    """Helper: return (logger, string_io) capturing JSON lines."""
    buf = io.StringIO()
    log = AgentLogger(logger_name, **logger_kwargs)
    # Patch the internal file/stdout write by redirecting _emit output
    log._file_handle = buf
    return log, buf


def _lines(buf: io.StringIO):
    """Parse all non-empty lines in buf as JSON, return list of dicts."""
    buf.seek(0)
    return [json.loads(line) for line in buf.getvalue().splitlines() if line.strip()]


# ──────────────────────────────────────────────────────────────────────────────
# Redactor
# ──────────────────────────────────────────────────────────────────────────────

class TestRedactor(unittest.TestCase):

    def test_redacts_openai_api_key(self):
        key = "sk-" + "a" * 32
        result = redact_string(f"Authorization: {key}")
        self.assertIn("[REDACTED:api_key]", result)
        self.assertNotIn(key, result)

    def test_redacts_github_token(self):
        token = "ghp_abcdefghijklmnopqrstuvwxyz123456"
        result = redact_string(token)
        self.assertIn("[REDACTED:gh_token]", result)

    def test_redacts_bearer_token(self):
        header = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.payload.sig"
        result = redact_string(header)
        self.assertIn("Bearer [REDACTED]", result)
        self.assertNotIn("eyJ", result)

    def test_does_not_redact_safe_string(self):
        safe = "This is a normal log message with no secrets."
        self.assertEqual(redact_string(safe), safe)

    def test_redacts_secret_key_name(self):
        result = redact_value("API_KEY", "mysecretvalue")
        self.assertEqual(result, "[REDACTED]")

    def test_redacts_password_key_name(self):
        result = redact_value("db_password", "hunter2")
        self.assertEqual(result, "[REDACTED]")

    def test_does_not_redact_non_string_value(self):
        result = redact_value("count", 42)
        self.assertEqual(result, 42)

    def test_redact_dict_recursive(self):
        data = {
            "message": "Hello",
            "nested": {
                "api_key": "sk-" + "b" * 40,
            },
        }
        result = redact_dict(data)
        self.assertEqual(result["message"], "Hello")
        self.assertNotIn("sk-", result["nested"]["api_key"])

    def test_redact_dict_does_not_modify_keys(self):
        data = {"API_KEY": "value", "safe_key": "value"}
        result = redact_dict(data)
        self.assertIn("API_KEY", result)
        self.assertIn("safe_key", result)


# ──────────────────────────────────────────────────────────────────────────────
# Token costs
# ──────────────────────────────────────────────────────────────────────────────

class TestTokenCosts(unittest.TestCase):

    def test_known_model_calculates_cost(self):
        cost = _calculate_cost(1_000_000, 0, "claude-opus-4")
        self.assertAlmostEqual(cost, 15.0, places=4)

    def test_completion_cost(self):
        cost = _calculate_cost(0, 1_000_000, "claude-opus-4")
        self.assertAlmostEqual(cost, 75.0, places=4)

    def test_combined_cost(self):
        # 500 prompt tokens at $15/M + 100 completion at $75/M = 0.0075 + 0.0075 = 0.015 USD
        cost = _calculate_cost(500, 100, "claude-opus-4")
        expected = (500 / 1_000_000 * 15.0) + (100 / 1_000_000 * 75.0)
        self.assertAlmostEqual(cost, expected, places=8)

    def test_unknown_model_returns_none(self):
        cost = _calculate_cost(1000, 500, "unknown-model-x")
        self.assertIsNone(cost)

    def test_none_model_returns_none(self):
        cost = _calculate_cost(1000, 500, None)
        self.assertIsNone(cost)

    def test_prefix_model_resolves(self):
        # "claude-opus-4-20250514" should resolve to "claude-opus-4"
        cost = _calculate_cost(1_000_000, 0, "claude-opus-4-20250514")
        self.assertAlmostEqual(cost, 15.0, places=4)

    def test_all_listed_models_have_costs(self):
        for model in TOKEN_COSTS:
            cost = _calculate_cost(1000, 1000, model)
            self.assertIsNotNone(cost)
            self.assertGreater(cost, 0)


# ──────────────────────────────────────────────────────────────────────────────
# Session — unique IDs
# ──────────────────────────────────────────────────────────────────────────────

class TestSessionIds(unittest.TestCase):

    def test_sessions_have_unique_ids(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session(task="task-a"):
            pass
        with log.session(task="task-b"):
            pass
        events = _lines(buf)
        starts = [e for e in events if e["event"] == "session_start"]
        self.assertEqual(len(starts), 2)
        self.assertNotEqual(starts[0]["session_id"], starts[1]["session_id"])

    def test_session_id_is_uuid4_format(self):
        import re
        log, buf = _capture_jsonl("agent-test")
        with log.session():
            pass
        events = _lines(buf)
        sid = events[0]["session_id"]
        uuid4_pattern = re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
        )
        self.assertRegex(sid, uuid4_pattern)


# ──────────────────────────────────────────────────────────────────────────────
# Span timing
# ──────────────────────────────────────────────────────────────────────────────

class TestSpanTiming(unittest.TestCase):

    def test_span_duration_is_positive(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("test_span"):
                time.sleep(0.01)
        events = _lines(buf)
        span_end = next(e for e in events if e["event"] == "span_end")
        self.assertGreater(span_end["duration_ms"], 0)

    def test_span_duration_is_approximate(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("slow_span"):
                time.sleep(0.05)
        events = _lines(buf)
        span_end = next(e for e in events if e["event"] == "span_end")
        # Allow generous tolerance for slow CI environments
        self.assertGreaterEqual(span_end["duration_ms"], 40)

    def test_span_name_in_event(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("my_special_span"):
                pass
        events = _lines(buf)
        span_end = next(e for e in events if e["event"] == "span_end")
        self.assertEqual(span_end["span"], "my_special_span")


# ──────────────────────────────────────────────────────────────────────────────
# Token tracking and cost calculation in spans
# ──────────────────────────────────────────────────────────────────────────────

class TestTokenTracking(unittest.TestCase):

    def test_tokens_recorded_in_span_end(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("llm_call") as span:
                span.tokens(prompt=500, completion=100, model="claude-opus-4")
        events = _lines(buf)
        span_end = next(e for e in events if e["event"] == "span_end")
        self.assertEqual(span_end["tokens"]["prompt"], 500)
        self.assertEqual(span_end["tokens"]["completion"], 100)
        self.assertEqual(span_end["tokens"]["total"], 600)

    def test_cost_calculated_in_span(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("llm_call") as span:
                span.tokens(prompt=1_000_000, completion=0, model="claude-opus-4")
        events = _lines(buf)
        span_end = next(e for e in events if e["event"] == "span_end")
        self.assertIn("cost_usd", span_end)
        self.assertAlmostEqual(span_end["cost_usd"], 15.0, places=4)

    def test_total_tokens_aggregated_in_session_end(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("call_1") as span:
                span.tokens(prompt=200, completion=50, model="gpt-4o")
            with session.span("call_2") as span:
                span.tokens(prompt=300, completion=100, model="gpt-4o")
        events = _lines(buf)
        session_end = next(e for e in events if e["event"] == "session_end")
        self.assertEqual(session_end["total_tokens"]["prompt"], 500)
        self.assertEqual(session_end["total_tokens"]["completion"], 150)
        self.assertEqual(session_end["total_tokens"]["total"], 650)

    def test_total_cost_aggregated_in_session_end(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("call_1") as span:
                span.tokens(prompt=1_000_000, completion=0, model="gpt-4o")
            with session.span("call_2") as span:
                span.tokens(prompt=0, completion=1_000_000, model="gpt-4o")
        events = _lines(buf)
        session_end = next(e for e in events if e["event"] == "session_end")
        # gpt-4o: $2.5/M prompt + $10/M completion = $12.5 total
        self.assertIn("total_cost_usd", session_end)
        self.assertAlmostEqual(session_end["total_cost_usd"], 12.5, places=4)

    def test_no_cost_when_model_unknown(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("call") as span:
                span.tokens(prompt=500, completion=100)
        events = _lines(buf)
        span_end = next(e for e in events if e["event"] == "span_end")
        self.assertNotIn("cost_usd", span_end)


# ──────────────────────────────────────────────────────────────────────────────
# JSON output is valid JSONL
# ──────────────────────────────────────────────────────────────────────────────

class TestJsonlOutput(unittest.TestCase):

    def test_all_lines_are_valid_json(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session(task="test") as session:
            session.info("Hello")
            session.warning("Careful")
            with session.span("op") as span:
                span.tokens(prompt=100, completion=50, model="gpt-4o-mini")
            session.tool_call("write_file", args={"path": "/tmp/x"}, result_summary="ok")
            session.decision("Use write_file because path exists")
        buf.seek(0)
        for line in buf.getvalue().splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)  # Will raise if invalid
            self.assertIn("event", obj)
            self.assertIn("session_id", obj)
            self.assertIn("ts", obj)

    def test_session_start_has_task(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session(task="my task"):
            pass
        events = _lines(buf)
        start = next(e for e in events if e["event"] == "session_start")
        self.assertEqual(start["task"], "my task")

    def test_agent_name_in_events(self):
        log, buf = _capture_jsonl("my-cool-agent")
        with log.session():
            pass
        events = _lines(buf)
        for event in events:
            self.assertEqual(event["agent"], "my-cool-agent")


# ──────────────────────────────────────────────────────────────────────────────
# Text format output
# ──────────────────────────────────────────────────────────────────────────────

class TestTextFormat(unittest.TestCase):

    def _capture_text(self):
        buf = io.StringIO()
        log = AgentLogger("agent-test", format="text")
        log._file_handle = buf
        return log, buf

    def test_text_format_session_start(self):
        log, buf = self._capture_text()
        with log.session(task="do stuff"):
            pass
        buf.seek(0)
        output = buf.getvalue()
        self.assertIn("SESSION START", output)
        self.assertIn("do stuff", output)

    def test_text_format_session_end(self):
        log, buf = self._capture_text()
        with log.session():
            pass
        buf.seek(0)
        self.assertIn("SESSION END", buf.getvalue())

    def test_text_format_info(self):
        log, buf = self._capture_text()
        with log.session() as session:
            session.info("Processing input")
        buf.seek(0)
        self.assertIn("INFO", buf.getvalue())
        self.assertIn("Processing input", buf.getvalue())

    def test_text_format_tool_call(self):
        log, buf = self._capture_text()
        with log.session() as session:
            session.tool_call("my_tool")
        buf.seek(0)
        self.assertIn("TOOL", buf.getvalue())
        self.assertIn("my_tool", buf.getvalue())

    def test_text_format_decision(self):
        log, buf = self._capture_text()
        with log.session() as session:
            session.decision("choosing option A because B")
        buf.seek(0)
        self.assertIn("DECISION", buf.getvalue())
        self.assertIn("choosing option A", buf.getvalue())

    def test_text_format_span(self):
        log, buf = self._capture_text()
        with log.session() as session:
            with session.span("inference"):
                pass
        buf.seek(0)
        output = buf.getvalue()
        self.assertIn("SPAN", output)
        self.assertIn("inference", output)


# ──────────────────────────────────────────────────────────────────────────────
# Nested spans
# ──────────────────────────────────────────────────────────────────────────────

class TestNestedSpans(unittest.TestCase):

    def test_multiple_spans_in_session(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("span_a"):
                pass
            with session.span("span_b"):
                pass
        events = _lines(buf)
        span_ends = [e for e in events if e["event"] == "span_end"]
        self.assertEqual(len(span_ends), 2)
        names = {e["span"] for e in span_ends}
        self.assertIn("span_a", names)
        self.assertIn("span_b", names)

    def test_spans_in_session_summary(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("alpha") as span:
                span.tokens(prompt=100, completion=50, model="gpt-4o-mini")
            with session.span("beta"):
                pass
        events = _lines(buf)
        session_end = next(e for e in events if e["event"] == "session_end")
        span_names = [s["name"] for s in session_end["spans"]]
        self.assertIn("alpha", span_names)
        self.assertIn("beta", span_names)


# ──────────────────────────────────────────────────────────────────────────────
# Tool call logging
# ──────────────────────────────────────────────────────────────────────────────

class TestToolCallLogging(unittest.TestCase):

    def test_tool_call_event_emitted(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            session.tool_call("search_web", args={"query": "AI news"}, result_summary="10 results", duration_ms=120)
        events = _lines(buf)
        tool_event = next(e for e in events if e["event"] == "tool_call")
        self.assertEqual(tool_event["tool"], "search_web")
        self.assertEqual(tool_event["args"]["query"], "AI news")
        self.assertEqual(tool_event["result_summary"], "10 results")
        self.assertEqual(tool_event["duration_ms"], 120)

    def test_tool_call_in_session_summary(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            session.tool_call("read_file", args={"path": "/tmp/x"})
        events = _lines(buf)
        session_end = next(e for e in events if e["event"] == "session_end")
        self.assertEqual(len(session_end["tool_calls"]), 1)
        self.assertEqual(session_end["tool_calls"][0]["tool"], "read_file")

    def test_tool_call_without_optional_fields(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            session.tool_call("ping")
        events = _lines(buf)
        tool_event = next(e for e in events if e["event"] == "tool_call")
        self.assertEqual(tool_event["tool"], "ping")


# ──────────────────────────────────────────────────────────────────────────────
# Decision logging
# ──────────────────────────────────────────────────────────────────────────────

class TestDecisionLogging(unittest.TestCase):

    def test_decision_event_emitted(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            session.decision("Choosing tool A because it handles binary files")
        events = _lines(buf)
        decision_event = next(e for e in events if e["event"] == "decision")
        self.assertIn("Choosing tool A", decision_event["reasoning"])

    def test_decisions_in_session_summary(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            session.decision("First reasoning step")
            session.decision("Second reasoning step")
        events = _lines(buf)
        session_end = next(e for e in events if e["event"] == "session_end")
        self.assertEqual(len(session_end["decisions"]), 2)
        self.assertIn("First reasoning step", session_end["decisions"])


# ──────────────────────────────────────────────────────────────────────────────
# Session summary completeness
# ──────────────────────────────────────────────────────────────────────────────

class TestSessionSummary(unittest.TestCase):

    def test_session_end_has_required_fields(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session(task="complete test") as session:
            session.info("step 1")
            with session.span("llm") as span:
                span.tokens(prompt=100, completion=50, model="claude-haiku-4")
            session.tool_call("run_code", args={"code": "print(1)"}, result_summary="1")
            session.decision("run_code is the best approach")

        events = _lines(buf)
        end = next(e for e in events if e["event"] == "session_end")

        required_keys = [
            "event", "session_id", "agent", "duration_ms",
            "spans", "tool_calls", "decisions", "total_tokens", "ts",
        ]
        for key in required_keys:
            self.assertIn(key, end, f"Missing key: {key}")

    def test_session_end_duration_positive(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session():
            time.sleep(0.005)
        events = _lines(buf)
        end = next(e for e in events if e["event"] == "session_end")
        self.assertGreater(end["duration_ms"], 0)

    def test_session_end_has_cost_when_model_known(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("call") as span:
                span.tokens(prompt=1000, completion=500, model="gpt-4o")
        events = _lines(buf)
        end = next(e for e in events if e["event"] == "session_end")
        self.assertIn("total_cost_usd", end)

    def test_session_end_no_cost_when_no_model(self):
        log, buf = _capture_jsonl("agent-test")
        with log.session() as session:
            with session.span("call") as span:
                span.tokens(prompt=1000, completion=500)
        events = _lines(buf)
        end = next(e for e in events if e["event"] == "session_end")
        self.assertNotIn("total_cost_usd", end)

    def test_redaction_in_session_output(self):
        log, buf = _capture_jsonl("agent-test", redact=True)
        api_key = "sk-" + "x" * 40
        with log.session() as session:
            session.info(f"Using key: {api_key}")
        events = _lines(buf)
        info_event = next(e for e in events if e["event"] == "info")
        self.assertNotIn(api_key, info_event["message"])
        self.assertIn("[REDACTED:api_key]", info_event["message"])


if __name__ == "__main__":
    unittest.main()
