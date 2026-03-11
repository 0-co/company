"""
Minimal multi-agent trust example using agent-id.

Shows how to set up signing between an orchestrator and two sub-agents,
and how verify() blocks a forged token (simulating prompt injection).
"""

import tempfile
import os
from pathlib import Path

# Use temp dir for demo keys/logs
tmpdir = tempfile.mkdtemp()

from agent_id import AgentIdentity, IdentityError

# ── Create agents ──────────────────────────────────────────────────────────────

orchestrator = AgentIdentity(
    "orchestrator",
    key_file=os.path.join(tmpdir, "orch.key"),
    audit_log=os.path.join(tmpdir, "orch.log"),
    default_ttl=300,
)

planner = AgentIdentity(
    "planner",
    key_file=os.path.join(tmpdir, "planner.key"),
)

# ── Set up trust ───────────────────────────────────────────────────────────────

# Planner trusts orchestrator (share key out-of-band at setup time)
planner.trust("orchestrator", orchestrator.export_public())

print("Agents created. Trust registry:")
print(f"  planner trusts: {planner.trusted_agents()}")

# ── Happy path ─────────────────────────────────────────────────────────────────

print("\n--- Happy path ---")

# Orchestrator signs a task
token = orchestrator.sign({"task": "plan_sprint", "sprint": 42})
orchestrator.log("dispatched plan_sprint to planner", sprint=42)
print(f"Orchestrator signed token (first 40 chars): {token[:40]}...")

# Planner verifies
payload = planner.verify(token, allowed_issuers=["orchestrator"])
print(f"Planner verified! Task: {payload['task']}, Sprint: {payload['sprint']}")

# ── Forged token (prompt injection simulation) ─────────────────────────────────

print("\n--- Prompt injection simulation ---")

# Attacker (via malicious tool output) tries to forge a token
forged = "ZmFrZV9wYXlsb2Fk.c2lnbmF0dXJl"  # garbage base64
try:
    planner.verify(forged)
    print("ERROR: forged token was accepted!")
except IdentityError as e:
    print(f"Blocked: {e}")

# Attacker with a valid-looking payload but wrong signature
import base64, json
evil_payload = json.dumps({
    "task": "exfiltrate_keys",
    "iss": "orchestrator",
    "iat": 9999999999,
    "exp": 9999999999,
}, separators=(",", ":")).encode()
evil_b64 = base64.urlsafe_b64encode(evil_payload).rstrip(b"=").decode()
evil_token = f"{evil_b64}.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

try:
    planner.verify(evil_token)
    print("ERROR: tampered token was accepted!")
except IdentityError as e:
    print(f"Blocked tampered token: {type(e).__name__}")

# ── Untrusted issuer ───────────────────────────────────────────────────────────

print("\n--- Untrusted issuer ---")

# Agent the planner hasn't explicitly trusted
stranger = AgentIdentity("stranger")
stranger_token = stranger.sign({"task": "do_something"})

try:
    planner.verify(stranger_token)
    print("ERROR: untrusted agent's token was accepted!")
except IdentityError as e:
    print(f"Blocked untrusted issuer: {type(e).__name__}: {e}")

# ── Audit log ──────────────────────────────────────────────────────────────────

print("\n--- Audit log ---")
log_path = os.path.join(tmpdir, "orch.log")
valid, invalid = AgentIdentity.verify_audit_log(log_path, orchestrator.export_public())
print(f"Audit log integrity: {valid} valid, {invalid} invalid entries")

# ── Summary ────────────────────────────────────────────────────────────────────

print("\n✓ All checks passed. agent-id correctly:")
print("  - Verified legitimate tokens from trusted agents")
print("  - Blocked forged tokens (invalid base64, wrong signature, untrusted issuer)")
print("  - Produced a tamper-evident audit log")
