"""
Span — a timed child unit within a Session.

Tracks duration, token usage, and cost for a single operation
(typically one LLM call, tool execution, or retrieval step).
"""

import time
from typing import Any, Dict, List, Optional

# Cost per million tokens in USD, keyed by model name
TOKEN_COSTS: Dict[str, Dict[str, float]] = {
    "claude-opus-4":   {"prompt": 15.0,  "completion": 75.0},
    "claude-sonnet-4": {"prompt": 3.0,   "completion": 15.0},
    "claude-haiku-4":  {"prompt": 0.8,   "completion": 4.0},
    "gpt-4o":          {"prompt": 2.5,   "completion": 10.0},
    "gpt-4o-mini":     {"prompt": 0.15,  "completion": 0.60},
    "gpt-4-turbo":     {"prompt": 10.0,  "completion": 30.0},
}


def _calculate_cost(prompt_tokens: int, completion_tokens: int, model: Optional[str]) -> Optional[float]:
    """Return USD cost for the given token counts, or None if model is unknown."""
    if model is None:
        return None
    # Allow prefix matching so "claude-opus-4-20250514" still resolves
    for known_model, rates in TOKEN_COSTS.items():
        if model.startswith(known_model):
            prompt_cost = (prompt_tokens / 1_000_000) * rates["prompt"]
            completion_cost = (completion_tokens / 1_000_000) * rates["completion"]
            return round(prompt_cost + completion_cost, 8)
    return None


class Span:
    """
    Context manager representing a timed operation within a session.

    Usage:
        with session.span("llm_call", model="claude-opus-4") as span:
            response = call_api(...)
            span.tokens(prompt=500, completion=100, model="claude-opus-4")
    """

    def __init__(
        self,
        name: str,
        session_id: str,
        emitter,          # callable(event_dict) — provided by Session
        redact: bool = True,
        **metadata: Any,
    ) -> None:
        self.name = name
        self.session_id = session_id
        self._emitter = emitter
        self._redact = redact
        self.metadata = metadata

        self._start_ms: float = 0.0
        self._duration_ms: int = 0
        self._token_data: Dict[str, Any] = {}
        self._cost_usd: Optional[float] = None
        self._events: List[Dict[str, Any]] = []
        self._error: Optional[str] = None

    def __enter__(self) -> "Span":
        self._start_ms = time.monotonic() * 1000
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        end_ms = time.monotonic() * 1000
        self._duration_ms = int(end_ms - self._start_ms)

        if exc_val is not None:
            self._error = str(exc_val)

        self._emit_span_end()
        # Do not suppress exceptions
        return False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def tokens(self, prompt: int = 0, completion: int = 0, model: Optional[str] = None) -> None:
        """Record token usage for this span and calculate cost if model is known."""
        total = prompt + completion
        self._token_data = {
            "prompt": prompt,
            "completion": completion,
            "total": total,
        }
        if model:
            self._token_data["model"] = model
        self._cost_usd = _calculate_cost(prompt, completion, model)

    def info(self, message: str, **extra: Any) -> None:
        """Log an informational event scoped to this span."""
        self._emit_inline("info", message=message, **extra)

    def error(self, message: str, exc: Optional[Exception] = None, **extra: Any) -> None:
        """Log an error event scoped to this span."""
        if exc is not None:
            extra["exc"] = str(exc)
        self._emit_inline("error", message=message, **extra)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _emit_inline(self, event_type: str, **fields: Any) -> None:
        event: Dict[str, Any] = {
            "event": event_type,
            "session_id": self.session_id,
            "span": self.name,
            **fields,
        }
        self._emitter(event)

    def _emit_span_end(self) -> None:
        event: Dict[str, Any] = {
            "event": "span_end",
            "session_id": self.session_id,
            "span": self.name,
            "duration_ms": self._duration_ms,
        }
        if self._token_data:
            event["tokens"] = self._token_data
        if self._cost_usd is not None:
            event["cost_usd"] = self._cost_usd
        if self._error:
            event["error"] = self._error
        if self.metadata:
            event["metadata"] = self.metadata
        self._emitter(event)

    def to_summary(self) -> Dict[str, Any]:
        """Return a compact dict for inclusion in the session_end summary."""
        summary: Dict[str, Any] = {
            "name": self.name,
            "duration_ms": self._duration_ms,
        }
        if self._token_data:
            summary["tokens"] = self._token_data
        if self._cost_usd is not None:
            summary["cost_usd"] = self._cost_usd
        if self._error:
            summary["error"] = self._error
        return summary
