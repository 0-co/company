"""
Session — a bounded unit of agent work.

Each session has a unique ID, tracks all spans/tool_calls/decisions,
and emits a full summary JSON line on exit.
"""

import time
import uuid
from typing import Any, Dict, List, Optional

from .span import Span


class Session:
    """
    Context manager representing a single agent task run.

    On entry: emits session_start event.
    On exit:  emits session_end event with full summary.

    Usage:
        with log.session(task="summarize docs") as session:
            session.info("Starting")
            with session.span("llm_call", model="claude-opus-4") as span:
                span.tokens(prompt=500, completion=100, model="claude-opus-4")
            session.tool_call("read_file", args={"path": "/tmp/data.txt"})
            session.decision("Will summarize with the LLM")
    """

    def __init__(
        self,
        agent_name: str,
        emitter,          # callable(event_dict)
        task: Optional[str] = None,
        redact: bool = True,
        **metadata: Any,
    ) -> None:
        self.session_id = str(uuid.uuid4())
        self.agent_name = agent_name
        self._emitter = emitter
        self._redact = redact
        self.task = task
        self.metadata = metadata

        self._start_ms: float = 0.0
        self._spans: List[Span] = []
        self._tool_calls: List[Dict[str, Any]] = []
        self._decisions: List[Dict[str, Any]] = []

    def __enter__(self) -> "Session":
        self._start_ms = time.monotonic() * 1000
        event: Dict[str, Any] = {
            "event": "session_start",
            "session_id": self.session_id,
            "agent": self.agent_name,
        }
        if self.task:
            event["task"] = self.task
        if self.metadata:
            event.update(self.metadata)
        self._emitter(event)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        duration_ms = int(time.monotonic() * 1000 - self._start_ms)
        self._emit_session_end(duration_ms, error=str(exc_val) if exc_val else None)
        return False

    # ------------------------------------------------------------------
    # Logging methods
    # ------------------------------------------------------------------

    def info(self, message: str, **extra: Any) -> None:
        """Log an informational event."""
        self._emit("info", message=message, **extra)

    def warning(self, message: str, **extra: Any) -> None:
        """Log a warning event."""
        self._emit("warning", message=message, **extra)

    def error(self, message: str, exc: Optional[Exception] = None, **extra: Any) -> None:
        """Log an error event, optionally attaching exception detail."""
        if exc is not None:
            extra["exc"] = str(exc)
        self._emit("error", message=message, **extra)

    def decision(self, reasoning: str, **extra: Any) -> None:
        """Log an agent reasoning or decision point."""
        record: Dict[str, Any] = {"reasoning": reasoning, **extra}
        self._decisions.append(record)
        self._emit("decision", reasoning=reasoning, **extra)

    def tool_call(
        self,
        name: str,
        args: Optional[Dict[str, Any]] = None,
        result_summary: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ) -> None:
        """Log a tool invocation with optional args, result summary, and timing."""
        record: Dict[str, Any] = {"tool": name}
        if args is not None:
            record["args"] = args
        if result_summary is not None:
            record["result_summary"] = result_summary
        if duration_ms is not None:
            record["duration_ms"] = duration_ms
        self._tool_calls.append(record)
        self._emit("tool_call", **record)

    def span(self, name: str, **metadata: Any) -> Span:
        """Create a child span context manager and register it for summary."""
        child_span = Span(
            name=name,
            session_id=self.session_id,
            emitter=self._emitter,
            redact=self._redact,
            **metadata,
        )
        self._spans.append(child_span)
        return child_span

    # ------------------------------------------------------------------
    # Token aggregation helpers
    # ------------------------------------------------------------------

    def _total_tokens(self) -> Dict[str, int]:
        prompt = sum(s._token_data.get("prompt", 0) for s in self._spans)
        completion = sum(s._token_data.get("completion", 0) for s in self._spans)
        return {"prompt": prompt, "completion": completion, "total": prompt + completion}

    def _total_cost(self) -> Optional[float]:
        costs = [s._cost_usd for s in self._spans if s._cost_usd is not None]
        if not costs:
            return None
        return round(sum(costs), 8)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _emit(self, event_type: str, **fields: Any) -> None:
        event: Dict[str, Any] = {
            "event": event_type,
            "session_id": self.session_id,
            **fields,
        }
        self._emitter(event)

    def _emit_session_end(self, duration_ms: int, error: Optional[str]) -> None:
        total_tokens = self._total_tokens()
        total_cost = self._total_cost()

        event: Dict[str, Any] = {
            "event": "session_end",
            "session_id": self.session_id,
            "agent": self.agent_name,
            "duration_ms": duration_ms,
            "spans": [s.to_summary() for s in self._spans],
            "tool_calls": self._tool_calls,
            "decisions": [d["reasoning"] for d in self._decisions],
            "total_tokens": total_tokens,
        }
        if self.task:
            event["task"] = self.task
        if total_cost is not None:
            event["total_cost_usd"] = total_cost
        if error:
            event["error"] = error
        self._emitter(event)
