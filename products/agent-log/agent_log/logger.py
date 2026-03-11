"""
AgentLogger — the main entry point for agent-log.

Manages output destination, format, redaction, and session creation.
All log events flow through the emitter configured here.
"""

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, IO, Optional

from .redactor import redact_dict
from .session import Session


def _utc_now() -> str:
    """Return current UTC time as an ISO-8601 string with Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _format_text(event: Dict[str, Any]) -> str:
    """
    Render a single event as a human-readable text line.
    Format: [TIMESTAMP] [AGENT] [SESSION_ID_PREFIX] EVENT_TYPE ...details
    """
    ts = event.get("ts", _utc_now())
    agent = event.get("agent", "agent")
    sid = event.get("session_id", "")[:8]
    etype = event.get("event", "info").upper()

    parts = [f"[{ts}]", f"[{agent}]", f"[{sid}]"]

    if etype == "SESSION_START":
        task = event.get("task", "")
        parts.append(f"SESSION START task={task}")

    elif etype == "SESSION_END":
        ms = event.get("duration_ms", 0)
        tokens = event.get("total_tokens", {}).get("total", 0)
        cost = event.get("total_cost_usd")
        cost_str = f" cost=${cost:.6f}" if cost is not None else ""
        parts.append(f"SESSION END duration={ms}ms tokens={tokens}{cost_str}")

    elif etype == "SPAN_END":
        span_name = event.get("span", "")
        ms = event.get("duration_ms", 0)
        tokens = event.get("tokens", {}).get("total", 0)
        cost = event.get("cost_usd")
        cost_str = f" cost=${cost:.6f}" if cost is not None else ""
        token_str = f" tokens={tokens}" if tokens else ""
        parts.append(f"SPAN {span_name} duration={ms}ms{token_str}{cost_str}")

    elif etype == "TOOL_CALL":
        tool = event.get("tool", "")
        ms = event.get("duration_ms")
        ms_str = f" {ms}ms" if ms is not None else ""
        parts.append(f"TOOL {tool}{ms_str}")

    elif etype == "DECISION":
        reasoning = event.get("reasoning", "")
        parts.append(f"DECISION {reasoning}")

    elif etype in ("INFO", "WARNING", "ERROR"):
        span = event.get("span")
        prefix = f"[{span}] " if span else ""
        message = event.get("message", "")
        parts.append(f"{etype} {prefix}{message}")

    else:
        parts.append(etype)

    return " ".join(parts)


class AgentLogger:
    """
    Structured logger for AI agent runs.

    Usage:
        log = AgentLogger("my-agent")
        with log.session(task="summarize docs") as session:
            session.info("Starting")
    """

    def __init__(
        self,
        name: str,
        output: Optional[str] = None,
        level: str = "INFO",
        format: str = "json",
        redact: bool = True,
    ) -> None:
        """
        Args:
            name:   Agent name, included in every emitted event.
            output: None = stdout; string = file path to append to.
            level:  "DEBUG", "INFO", "WARNING", "ERROR" (currently informational).
            format: "json" (JSONL) or "text" (human-readable).
            redact: If True, auto-redact API keys and secrets from string values.
        """
        self.name = name
        self.level = level.upper()
        self.format = format.lower()
        self.redact = redact
        self._output_path = output
        self._file_handle: Optional[IO[str]] = None

        if output is not None:
            self._file_handle = open(output, "a", encoding="utf-8")

    def session(self, task: Optional[str] = None, **metadata: Any) -> Session:
        """Create and return a Session context manager."""
        return Session(
            agent_name=self.name,
            emitter=self._emit,
            task=task,
            redact=self.redact,
            **metadata,
        )

    def configure(
        self,
        output: Optional[str] = None,
        level: Optional[str] = None,
        format: Optional[str] = None,
        redact: Optional[bool] = None,
    ) -> None:
        """Update logger settings at runtime."""
        if level is not None:
            self.level = level.upper()
        if format is not None:
            self.format = format.lower()
        if redact is not None:
            self.redact = redact
        if output is not None and output != self._output_path:
            if self._file_handle:
                self._file_handle.close()
            self._output_path = output
            self._file_handle = open(output, "a", encoding="utf-8")

    def close(self) -> None:
        """Flush and close the output file handle if one is open."""
        if self._file_handle:
            self._file_handle.flush()
            self._file_handle.close()
            self._file_handle = None

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _emit(self, event: Dict[str, Any]) -> None:
        """Redact, timestamp, serialize, and write a single event."""
        event["ts"] = _utc_now()
        # Ensure agent name is present on every event
        if "agent" not in event:
            event["agent"] = self.name

        if self.redact:
            event = redact_dict(event)

        line = self._serialize(event)
        dest = self._file_handle if self._file_handle else sys.stdout
        dest.write(line + "\n")
        dest.flush()

    def _serialize(self, event: Dict[str, Any]) -> str:
        if self.format == "text":
            return _format_text(event)
        return json.dumps(event, default=str)
