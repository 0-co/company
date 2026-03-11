"""Span — the basic unit of a trace."""

import json
import os
import time
from typing import Any, Dict, List, Optional


def _generate_id(num_bytes: int) -> str:
    return os.urandom(num_bytes).hex()


class Span:
    """A single unit of work in a trace.

    Created by Tracer.start_span(). Use as a context manager — end_time is set
    on __exit__.
    """

    def __init__(
        self,
        name: str,
        trace_id: str,
        parent_span_id: Optional[str] = None,
    ) -> None:
        self.span_id: str = _generate_id(4)  # 8-char hex
        self.trace_id: str = trace_id
        self.parent_span_id: Optional[str] = parent_span_id
        self.name: str = name
        self.start_time: float = time.time()
        self.end_time: Optional[float] = None
        self.attributes: Dict[str, Any] = {}
        self.events: List[Dict[str, Any]] = []
        self.status: str = "ok"
        self.error_message: Optional[str] = None

    def set_attribute(self, key: str, value: Any) -> None:
        """Store an arbitrary key-value attribute on this span."""
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Record a timestamped event on this span."""
        self.events.append(
            {
                "name": name,
                "timestamp": time.time(),
                "attributes": attributes or {},
            }
        )

    def record_error(self, exc: Exception) -> None:
        """Mark this span as failed and store exception details."""
        self.status = "error"
        self.error_message = str(exc)
        self.add_event(
            "error",
            {
                "exception.type": type(exc).__name__,
                "exception.message": str(exc),
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict of this span."""
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "attributes": self.attributes,
            "events": self.events,
            "status": self.status,
            "error_message": self.error_message,
        }

    def __enter__(self) -> "Span":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.end_time = time.time()
        if exc_type is not None and self.status != "error":
            self.status = "error"
            if exc_val is not None:
                self.error_message = str(exc_val)
        # Let exceptions propagate normally.
        return None

    def __repr__(self) -> str:
        return (
            f"Span(name={self.name!r}, span_id={self.span_id!r}, "
            f"trace_id={self.trace_id!r}, status={self.status!r})"
        )
