"""Tracer — creates and tracks spans for a single trace."""

import os
from typing import Any, Dict, List, Optional

from .span import Span
from .context import _push_span, _pop_span, get_current_span


def _generate_trace_id() -> str:
    return os.urandom(8).hex()  # 16-char hex


class _SpanContextManager:
    """Wraps a Span so that push/pop on the thread-local stack happens here,
    not inside Span itself (keeping Span free of tracer-level concerns)."""

    def __init__(self, span: Span, tracer: "Tracer") -> None:
        self._span = span
        self._tracer = tracer

    def __enter__(self) -> Span:
        _push_span(self._span, self._tracer)
        return self._span

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # Close the span (sets end_time, status).
        self._span.__exit__(exc_type, exc_val, exc_tb)
        # Pop from thread-local stack.
        _pop_span()
        # Record completed span.
        self._tracer._completed_spans.append(self._span)
        return None


class Tracer:
    """Manages spans for a single distributed trace.

    Usage::

        tracer = Tracer()
        with tracer.start_span("my_op") as span:
            span.set_attribute("model", "claude-sonnet-4-6")
    """

    def __init__(self, trace_id: Optional[str] = None) -> None:
        self.trace_id: str = trace_id or _generate_trace_id()
        self._completed_spans: List[Span] = []
        # When created via from_context(), the first span's parent comes from here.
        self._remote_parent_span_id: Optional[str] = None

    def start_span(
        self,
        name: str,
        parent_span_id: Optional[str] = None,
    ) -> _SpanContextManager:
        """Create a new span.

        Parent resolution order:
        1. Explicit parent_span_id argument.
        2. Current top-of-stack span for this thread.
        3. Remote parent set via from_context() (consumed once).
        """
        if parent_span_id is None:
            current = get_current_span()
            if current is not None and current.trace_id == self.trace_id:
                parent_span_id = current.span_id
            elif self._remote_parent_span_id is not None:
                parent_span_id = self._remote_parent_span_id
                # Consume it — only the first span inherits the remote parent.
                self._remote_parent_span_id = None

        span = Span(name=name, trace_id=self.trace_id, parent_span_id=parent_span_id)
        return _SpanContextManager(span, self)

    def get_context(self) -> Dict[str, Any]:
        """Return a serializable context dict for passing to another process/agent."""
        current = get_current_span()
        span_id = current.span_id if current is not None else None
        return {
            "trace_id": self.trace_id,
            "span_id": span_id,
            "baggage": {},
        }

    @classmethod
    def from_context(cls, ctx: Dict[str, Any]) -> "Tracer":
        """Continue an existing trace received from another process/agent."""
        tracer = cls(trace_id=ctx["trace_id"])
        tracer._remote_parent_span_id = ctx.get("span_id")
        return tracer

    def get_spans(self) -> List[Dict[str, Any]]:
        """Return all completed spans as serializable dicts."""
        return [span.to_dict() for span in self._completed_spans]

    def export_jsonl(self, path: str) -> None:
        """Append each completed span as a JSON line to path."""
        import json

        with open(path, "a", encoding="utf-8") as fh:
            for span in self._completed_spans:
                fh.write(json.dumps(span.to_dict()) + "\n")

    def get_trace_tree(self) -> Dict[str, Any]:
        """Return the spans as a nested tree.

        Root nodes are spans with no parent (or whose parent is outside this
        tracer's completed spans). Each node has a 'children' list.
        """
        spans_by_id: Dict[str, Dict[str, Any]] = {}
        for span in self._completed_spans:
            node = span.to_dict()
            node["children"] = []
            spans_by_id[span.span_id] = node

        roots: List[Dict[str, Any]] = []
        known_ids = set(spans_by_id.keys())

        for node in spans_by_id.values():
            parent_id = node.get("parent_span_id")
            if parent_id and parent_id in known_ids:
                spans_by_id[parent_id]["children"].append(node)
            else:
                roots.append(node)

        if len(roots) == 1:
            return roots[0]
        return {"children": roots, "trace_id": self.trace_id}
