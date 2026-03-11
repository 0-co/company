"""agent-trace — distributed tracing for multi-agent workflows.

Zero dependencies. Works with any agent framework.
"""

import asyncio
import functools
from typing import Any, Callable, Optional

from .span import Span
from .tracer import Tracer
from .context import get_current_span, get_current_tracer
from .export import spans_to_jsonl, write_jsonl, read_jsonl

__version__ = "0.1.0"
__all__ = [
    "Tracer",
    "Span",
    "trace_span",
    "get_current_span",
    "get_current_tracer",
    "spans_to_jsonl",
    "write_jsonl",
    "read_jsonl",
]


def trace_span(name: Optional[Any] = None) -> Any:
    """Decorator for sync and async functions.

    Automatically creates or reuses a Tracer. Supports both forms::

        @trace_span
        def my_fn(): ...

        @trace_span("custom_name")
        async def my_async_fn(): ...
    """

    def decorator(fn: Callable) -> Callable:
        span_name: str = _name if isinstance(_name, str) else fn.__name__

        if asyncio.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = get_current_tracer() or Tracer()
                with tracer.start_span(span_name):
                    return await fn(*args, **kwargs)

            return async_wrapper
        else:

            @functools.wraps(fn)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                tracer = get_current_tracer() or Tracer()
                with tracer.start_span(span_name):
                    return fn(*args, **kwargs)

            return sync_wrapper

    # Support @trace_span (no call) and @trace_span("name") (called with string).
    if callable(name):
        # @trace_span — name is actually the function
        _name = name.__name__
        return decorator(name)

    # @trace_span("name") — name is a string (or None)
    _name = name
    return decorator
