"""
agent-id: Zero-dependency agent identity and trust verification.

Drop-in trust layer for multi-agent systems. Signs agent calls with HMAC-SHA256,
verifies signatures before acting, maintains an append-only audit log.

Solves the prompt injection / confused deputy problem:
    How does sub-agent B know instructions came from orchestrator A,
    and not from a malicious tool output pretending to be A?

Usage:
    from agent_id import AgentIdentity

    # Orchestrator: create identity
    orch = AgentIdentity("orchestrator", key_file=".agent-keys/orch.key")

    # Sign instructions to sub-agents
    token = orch.sign({"action": "run_analysis", "target": "planner"})

    # Sub-agent: verify before acting
    planner = AgentIdentity("planner", key_file=".agent-keys/planner.key")
    planner.trust("orchestrator", orch.export_public())
    payload = planner.verify(token)  # raises IdentityError if forged
"""

from .identity import AgentIdentity
from .exceptions import IdentityError, UntrustedIssuerError, ExpiredTokenError

__version__ = "0.1.0"
__all__ = ["AgentIdentity", "IdentityError", "UntrustedIssuerError", "ExpiredTokenError"]
