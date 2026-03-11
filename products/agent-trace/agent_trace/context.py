"""Thread-local context — current active span and tracer."""

import threading
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .span import Span
    from .tracer import Tracer

_local: threading.local = threading.local()


def get_current_span() -> Optional["Span"]:
    """Return the innermost active span for this thread, or None."""
    stack = getattr(_local, "span_stack", [])
    if not stack:
        return None
    return stack[-1]


def get_current_tracer() -> Optional["Tracer"]:
    """Return the active tracer for this thread, or None."""
    tracer_stack = getattr(_local, "tracer_stack", [])
    if not tracer_stack:
        return None
    return tracer_stack[-1]


def _push_span(span: "Span", tracer: "Tracer") -> None:
    """Internal: push a span and its owning tracer onto the thread-local stacks."""
    if not hasattr(_local, "span_stack"):
        _local.span_stack = []
        _local.tracer_stack = []
    _local.span_stack.append(span)
    _local.tracer_stack.append(tracer)


def _pop_span() -> Optional["Span"]:
    """Internal: pop the innermost span and tracer off the thread-local stacks."""
    stack = getattr(_local, "span_stack", [])
    tracer_stack = getattr(_local, "tracer_stack", [])
    if not stack:
        return None
    span = stack.pop()
    if tracer_stack:
        tracer_stack.pop()
    return span
