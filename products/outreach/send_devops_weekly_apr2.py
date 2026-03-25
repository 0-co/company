#!/usr/bin/env python3
"""
Send DevOps Weekly newsletter submission to gareth@morethanseven.net.
Scheduled: April 2, 2026 (after first week of cold email responses)
Run: python3 send_devops_weekly_apr2.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-02":
    print(f"[HOLD] Today is {today}. This email fires April 2.")
    exit(0)

# Fill in before sending
HN_UPVOTES = 0
HN_LINK = ""

body = """Hi Gareth,

Submitting a tool for DevOps Weekly: mcp-diff — schema lockfile and breaking change detector for MCP server deployments.

The problem: MCP servers serve tool schemas at runtime. When someone deploys an updated server, the schema changes silently — no diff, no CI failure, no notification to the teams whose agents depend on it. mcp-diff captures a snapshot (mcp-schema.lock) and fails CI if the schema drifts unexpectedly.

`pip install mcp-diff`, one YAML step in GitHub Actions, done.

Relevant to DevOps because this is a deploy-gate problem, not a development problem. The schemas are an API contract that agents depend on — nobody was treating them as such until now.

Companion tool: agent-friend (MCP schema linter, 156 checks, 201 servers graded) for build-time quality. mcp-diff is the deploy gate.

GitHub: https://github.com/0-co/mcp-diff
agent-friend: https://github.com/0-co/agent-friend"""

if HN_UPVOTES > 30 and HN_LINK:
    body += f"\n\nagent-friend got {HN_UPVOTES} upvotes on Show HN March 23 — some good discussion about when schema bloat is intentional vs accidental: {HN_LINK}"

body += """

— 0coCeo (I'm an autonomous AI running this company, but the tools are real)
https://github.com/0-co/mcp-diff"""

payload = {
    "to": "gareth@morethanseven.net",
    "subject": "Tool for DevOps Weekly: mcp-diff — schema lockfile for MCP server deployments",
    "text": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:400], "...")
print()
if HN_UPVOTES:
    print(f"HN: {HN_UPVOTES} pts | Link: {HN_LINK}")
print()
# Auto-send (date guard is the safety check)

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

if result.returncode == 0:
    ts = datetime.utcnow().strftime('%H:%MZ')
    print(f"\n✓ Sent. Log:")
    print(f"- [{ts}] outbound pitch: gareth@morethanseven.net — DevOps Weekly newsletter submission, mcp-diff")
