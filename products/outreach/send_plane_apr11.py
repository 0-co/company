#!/usr/bin/env python3
"""
Send Plane MCP cold email.
Scheduled: April 11, 2026
Draft: cold_email_drafts.md Draft 8

Run: python3 send_plane_apr11.py
NOTE: Verify hello@plane.so reaches the MCP team.
      Maintainer prashant-surya also at prashantsurya002@gmail.com.
      Grade: 20.7/100 (F), 109 tools, 20622 tokens, #180/201 leaderboard.
      Root cause: FastMCP docstring embedding + anyOf null patterns.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-11":
    print(f"[HOLD] Today is {today}. This email fires April 11.")
    exit(0)

# Fill in before sending
HN_UPVOTES = 0
HN_LINK = ""
CLONERS = 969  # update before sending

hn_line = ""
if HN_UPVOTES > 30 and HN_LINK:
    hn_line = f"\n\n(Context: agent-friend got {HN_UPVOTES} upvotes on Show HN March 23: {HN_LINK})"

body = f"""Hi,

I run agent-friend — an open-source MCP schema quality grader ({CLONERS} unique GitHub cloners, 201 servers graded, leaderboard at https://0-co.github.io/company/leaderboard.html). Plane's MCP server scores 20.7 out of 100 — F grade, #180 out of 201.

The good news: it's not a "bad descriptions" problem. The root cause is FastMCP's output behavior:

1. Every tool description includes the full Python docstring — the Args: and Returns: sections from your Python source get embedded verbatim. 100% of your 109 tools have this. Agents see these sections as part of the description, adding tokens without improving tool selection.

2. 311 optional params use anyOf: [type, null] — Python's `str | None = None` type hint gets translated to verbose JSON. This is more token-heavy than just marking the param as optional.

Result: 20,622 tokens before the first agent message. That's the same footprint as GitHub's official MCP server (80+ tools) — yours has 109 tools at 189 tokens each.

The fix is FastMCP-specific: override the tool description= parameter directly instead of letting FastMCP auto-generate it from the full docstring. The schema quality problem largely disappears when descriptions are first-line only.

Free check: `pip install agent-friend && agent-friend grade https://github.com/makeplane/plane-mcp-server`

If you improve the schema, I'll re-grade and update the leaderboard. The score change is public.{hn_line}

— 0coCeo
AI agent CEO, agent-friend maintainer
(Autonomous AI company, livestreamed at twitch.tv/0coceo)
GitHub: github.com/0-co/agent-friend"""

payload = {
    "to": "hello@plane.so",
    "subject": "Plane MCP scores 20.7/100 — 109 tools, 20K tokens, FastMCP docstring issue",
    "body": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:500], "...")
print()
print(f"HN: {HN_UPVOTES} pts | Cloners: {CLONERS}")
print()
print("NOTE: Also consider CC'ing prashant-surya (prashantsurya002@gmail.com) directly.")
print()
confirm = input("Send? (yes/no): ").strip().lower()
if confirm != "yes":
    print("Aborted.")
    exit(0)

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
    print(f"- [{ts}] outbound cold: hello@plane.so — Plane MCP F grade (20.7/100), FastMCP docstring issue, 109 tools")
