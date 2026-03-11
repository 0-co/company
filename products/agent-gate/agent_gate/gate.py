"""
Core gate logic for agent-gate.

Provides:
  - GateConfig — configuration dataclass
  - Gate — class with confirm() method and @gate.requires() decorator
  - gate — module-level default Gate instance
"""

import asyncio
import functools
import inspect
import sys
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .exceptions import ActionDenied, GateTimeout


# ---------------------------------------------------------------------------
# Approval handlers
# ---------------------------------------------------------------------------

class StdinApprovalHandler:
    """
    Prompts for approval on stdin/stderr.

    Suitable for CLI tools and interactive agents.
    Blocks the calling thread while waiting.
    """

    def __init__(self, timeout: Optional[float] = None) -> None:
        self.timeout = timeout

    def request(self, action: str, context: Dict[str, Any]) -> bool:
        """Print prompt and wait for y/n. Returns True for approved."""
        print(f"\n[agent-gate] Action requires approval:", file=sys.stderr)
        print(f"  {action}", file=sys.stderr)
        if context:
            for k, v in context.items():
                print(f"  {k}: {v}", file=sys.stderr)

        if self.timeout is not None:
            print(f"  (auto-deny in {self.timeout:.0f}s)", file=sys.stderr)

        result_holder: List[Optional[bool]] = [None]
        done = threading.Event()

        def _read_input() -> None:
            try:
                raw = input("  Approve? [y/N] ").strip().lower()
                result_holder[0] = raw in ("y", "yes")
            except (EOFError, KeyboardInterrupt):
                result_holder[0] = False
            finally:
                done.set()

        t = threading.Thread(target=_read_input, daemon=True)
        t.start()

        if self.timeout is not None:
            done.wait(timeout=self.timeout)
            if not done.is_set():
                print(f"\n  [timeout — action denied]", file=sys.stderr)
                return False
        else:
            done.wait()

        return bool(result_holder[0])


class AutoApproveHandler:
    """
    Automatically approves all actions. Useful for testing.

    WARNING: disables the safety gate entirely. Use only in tests.
    """

    def request(self, action: str, context: Dict[str, Any]) -> bool:
        return True


class AutoDenyHandler:
    """
    Automatically denies all actions. Useful for CI and read-only contexts.
    """

    def request(self, action: str, context: Dict[str, Any]) -> bool:
        return False


class CallbackApprovalHandler:
    """
    Delegates approval to a user-supplied callable.

    The callable receives (action: str, context: dict) and must return True
    (approved) or False (denied). Useful for custom UIs, webhooks, etc.
    """

    def __init__(self, callback: Callable[[str, Dict[str, Any]], bool]) -> None:
        self.callback = callback

    def request(self, action: str, context: Dict[str, Any]) -> bool:
        return bool(self.callback(action, context))


# ---------------------------------------------------------------------------
# GateConfig
# ---------------------------------------------------------------------------

@dataclass
class GateConfig:
    """
    Configuration for a Gate.

    Parameters
    ----------
    handler : approval handler object
        Object with a ``request(action, context) -> bool`` method.
        Defaults to StdinApprovalHandler (interactive prompt).
    timeout : float, optional
        Seconds before the approval request auto-denies. None = no timeout.
        Only respected by StdinApprovalHandler; custom handlers must implement
        their own timeout if needed.
    log_decisions : bool
        If True, print a short log line for each gate decision to stderr.
    """

    handler: Any = field(default_factory=StdinApprovalHandler)
    timeout: Optional[float] = None
    log_decisions: bool = True


# ---------------------------------------------------------------------------
# Gate
# ---------------------------------------------------------------------------

class Gate:
    """
    Human-in-the-loop approval gate for AI agent actions.

    Usage::

        from agent_gate import Gate, ActionDenied

        gate = Gate()

        # Direct call
        gate.confirm("Send email to user@example.com", to="user@example.com")

        # Decorator
        @gate.requires("Send email")
        def send_email(to, subject, body):
            ...

        # Async decorator
        @gate.requires("Delete files", context={"path": "/data"})
        async def delete_files(path):
            ...

    Raises ActionDenied if the user declines.
    Raises GateTimeout if using StdinApprovalHandler with a timeout.
    """

    def __init__(self, config: Optional[GateConfig] = None, **kwargs: Any) -> None:
        if config is not None:
            self._config = config
        else:
            # Build from kwargs for convenience: Gate(timeout=30)
            handler = kwargs.pop("handler", None)
            if handler is None:
                timeout = kwargs.get("timeout")
                handler = StdinApprovalHandler(timeout=timeout)
            self._config = GateConfig(handler=handler, **kwargs)

    def _request(self, action: str, context: Dict[str, Any]) -> None:
        """Synchronously request approval. Raises ActionDenied on denial."""
        approved = self._config.handler.request(action, context)
        if self._config.log_decisions:
            status = "APPROVED" if approved else "DENIED"
            print(f"[agent-gate] {status}: {action}", file=sys.stderr)
        if not approved:
            raise ActionDenied(action)

    def confirm(self, action: str, **context: Any) -> None:
        """
        Request human approval synchronously.

        Parameters
        ----------
        action : str
            Human-readable description of the action to approve.
        **context :
            Additional context shown to the approver.

        Raises
        ------
        ActionDenied
            If the action is denied.
        GateTimeout
            If the request times out (StdinApprovalHandler with timeout set).
        """
        self._request(action, context)

    async def confirm_async(self, action: str, **context: Any) -> None:
        """
        Request human approval asynchronously (runs handler in thread).

        Same as confirm() but safe to call from async code without blocking
        the event loop.
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: self._request(action, context))

    def requires(
        self,
        action: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Callable:
        """
        Decorator that gates a function behind human approval.

        The decorated function is only called if the approver says yes.
        Raises ActionDenied otherwise.

        Parameters
        ----------
        action : str
            Description shown to the approver.
        context : dict, optional
            Additional context shown at the approval prompt. Can contain
            format strings referencing the decorated function's arguments,
            e.g. ``context={"to": "{to}", "subject": "{subject}"}`` will
            interpolate the function's `to` and `subject` arguments.

        Example::

            @gate.requires("Send email to {to}", context={"subject": "{subject}"})
            def send_email(to, subject, body):
                ...
        """
        ctx = context or {}

        def decorator(fn: Callable) -> Callable:
            sig = inspect.signature(fn)

            if inspect.iscoroutinefunction(fn):
                @functools.wraps(fn)
                async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                    bound = sig.bind(*args, **kwargs)
                    bound.apply_defaults()
                    all_args = dict(bound.arguments)
                    resolved_action = _format_template(action, all_args)
                    resolved_ctx = {k: _format_template(str(v), all_args) for k, v in ctx.items()}
                    await self.confirm_async(resolved_action, **resolved_ctx)
                    return await fn(*args, **kwargs)
                return async_wrapper
            else:
                @functools.wraps(fn)
                def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                    bound = sig.bind(*args, **kwargs)
                    bound.apply_defaults()
                    all_args = dict(bound.arguments)
                    resolved_action = _format_template(action, all_args)
                    resolved_ctx = {k: _format_template(str(v), all_args) for k, v in ctx.items()}
                    self.confirm(resolved_action, **resolved_ctx)
                    return fn(*args, **kwargs)
                return sync_wrapper

        return decorator


def _format_template(template: str, args: Dict[str, Any]) -> str:
    """Format a template string with function arguments, ignoring missing keys."""
    try:
        return template.format(**args)
    except (KeyError, ValueError):
        return template
