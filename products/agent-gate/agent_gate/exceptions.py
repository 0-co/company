"""
Exceptions for agent-gate.
"""


class ActionDenied(Exception):
    """
    Raised when a gated action is denied (either by the user or by policy).

    Attributes:
        action: Human-readable description of the denied action.
        reason: Why it was denied ('user_denied', 'timeout', 'auto_deny').
    """

    def __init__(self, action: str, reason: str = "user_denied") -> None:
        self.action = action
        self.reason = reason
        super().__init__(f"Action denied ({reason}): {action}")


class GateTimeout(ActionDenied):
    """
    Raised when the approval request times out before a decision is made.
    """

    def __init__(self, action: str, timeout: float) -> None:
        self.timeout = timeout
        super().__init__(action, reason="timeout")
        self.args = (f"Approval request timed out after {timeout}s: {action}",)
