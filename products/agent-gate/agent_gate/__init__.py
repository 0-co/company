"""
agent-gate — human-in-the-loop approval for AI agent actions.

Zero dependencies. Pure stdlib. Works with sync and async.

Quick start::

    from agent_gate import gate, ActionDenied

    # Direct confirmation
    gate.confirm("Send email to user@example.com")

    # Decorator
    @gate.requires("Delete {path}")
    def delete_file(path):
        os.remove(path)

    # Custom gate with auto-deny for CI
    from agent_gate import Gate, AutoDenyHandler
    ci_gate = Gate(handler=AutoDenyHandler())

    @ci_gate.requires("Irreversible action")
    def risky_operation():
        ...
"""

from .exceptions import ActionDenied, GateTimeout
from .gate import (
    AutoApproveHandler,
    AutoDenyHandler,
    CallbackApprovalHandler,
    Gate,
    GateConfig,
    StdinApprovalHandler,
)

__version__ = "0.1.0"

# Module-level default gate (stdin, no timeout).
gate = Gate()

__all__ = [
    "gate",
    "Gate",
    "GateConfig",
    "ActionDenied",
    "GateTimeout",
    "StdinApprovalHandler",
    "AutoApproveHandler",
    "AutoDenyHandler",
    "CallbackApprovalHandler",
]
