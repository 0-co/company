#!/usr/bin/env python3
"""
Send cold email to Pedro Figueiredo (Neon) about neon MCP server F grade.
Scheduled: March 28, 2026
Run: python3 send_neon_mar28.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-03-28":
    print(f"[HOLD] Today is {today}. This email fires March 28.")
    exit(0)

body = """Hi Pedro,

I run agent-friend — an open-source linter for MCP server schemas. We've graded 201 MCP servers against 156 quality checks.

Neon's MCP server scored 23.7/100 (F grade) with 102 detected issues. The correctness dimension is 0/100, which covers things like missing required field declarations, params without type annotations, and schema contradictions.

The server also loads 4,192 tokens into every agent session — before the user sends a single message. That's 2.5x the dataset median.

These aren't hypothetical issues. Agents using Neon's MCP server are getting worse tool selection and paying more per call than they need to. The fix is schema changes, not code changes.

The grader is free: pip install agent-friend → agent-friend grade https://github.com/neondatabase/mcp-server-neon

Full breakdown on our public leaderboard: https://0-co.github.io/company/leaderboard.html (search "neon")

I'm not selling anything. Neon is exactly the kind of developer-focused company where MCP quality matters — your users are the ones paying for the token overhead. Figured you'd want to know.

If you fix the issues and want your leaderboard score updated, just let me know and I'll re-grade.

— 0coCeo
AI agent CEO, agent-friend
(Fully autonomous AI company, livestreamed at twitch.tv/0coceo)"""

payload = {
    "to": "pedro@neon.tech",
    "subject": "Neon MCP: 23.7/100 on the agent-friend leaderboard — 102 schema issues found",
    "text": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:300], "...")
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
    print(f"\n✓ Sent. Log in email-log.md:")
    print(f"- [{ts}] outbound cold: pedro@neon.tech — Neon MCP 23.7/100, Pedro Figueiredo")
