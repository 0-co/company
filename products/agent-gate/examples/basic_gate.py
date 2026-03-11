"""
agent-gate basic examples — using AutoApproveHandler for non-interactive testing.

Run from the products/agent-gate directory:
  python examples/basic_gate.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_gate import (
    ActionDenied,
    AutoApproveHandler,
    AutoDenyHandler,
    CallbackApprovalHandler,
    Gate,
    GateConfig,
)

print("=== agent-gate basic examples ===\n")


# ── Example 1: auto-approve (testing mode) ────────────────────────────────────
gate_approve = Gate(handler=AutoApproveHandler())

print("Example 1: gate.confirm() with AutoApproveHandler")
gate_approve.confirm("Send email to test@example.com")
print("  Action approved and executed.")
print()


# ── Example 2: auto-deny ──────────────────────────────────────────────────────
gate_deny = Gate(handler=AutoDenyHandler())

print("Example 2: gate.confirm() with AutoDenyHandler")
try:
    gate_deny.confirm("Delete all production data")
    print("  ERROR: should have been denied")
except ActionDenied as e:
    print(f"  ActionDenied: {e.action} (reason: {e.reason})")
print()


# ── Example 3: @gate.requires decorator ──────────────────────────────────────
gate3 = Gate(handler=AutoApproveHandler())

@gate3.requires("Send email to {to}", context={"subject": "{subject}"})
def send_email(to: str, subject: str, body: str) -> str:
    return f"Email sent to {to}: {subject}"

print("Example 3: @gate.requires with arg interpolation")
result = send_email("user@example.com", "Hello", "Body text")
print(f"  Result: {result!r}")
print()


# ── Example 4: @gate.requires blocks on denial ────────────────────────────────
gate4 = Gate(handler=AutoDenyHandler())

@gate4.requires("Delete file {path}")
def delete_file(path: str) -> None:
    raise AssertionError("should not reach here")

print("Example 4: @gate.requires blocks on denial")
try:
    delete_file("/important/data.db")
    print("  ERROR: should have raised ActionDenied")
except ActionDenied as e:
    print(f"  ActionDenied before execution: {e.action}")
print()


# ── Example 5: custom callback handler ───────────────────────────────────────
approved_actions = []

def my_approval_callback(action: str, context: dict) -> bool:
    # In production: send Slack DM, check database policy, etc.
    allowed = "dangerous" not in action.lower()
    approved_actions.append((action, allowed))
    return allowed

gate5 = Gate(handler=CallbackApprovalHandler(my_approval_callback))

print("Example 5: CallbackApprovalHandler")
gate5.confirm("Send Twitch chat message")
try:
    gate5.confirm("Dangerous: wipe database")
except ActionDenied:
    pass
print(f"  Decisions: {approved_actions}")
print()


# ── Example 6: async gate ────────────────────────────────────────────────────
gate6 = Gate(handler=AutoApproveHandler())

@gate6.requires("Async API call to {endpoint}")
async def async_api_call(endpoint: str, data: dict) -> dict:
    return {"status": "ok", "endpoint": endpoint}

print("Example 6: async @gate.requires")
result = asyncio.run(async_api_call("/users/delete", {"id": 42}))
print(f"  Result: {result}")
print()


print("All examples passed.")
