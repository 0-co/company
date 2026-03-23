#!/usr/bin/env python3
"""
Send tool submission to Import Python newsletter.
Scheduled: April 4, 2026
Target: contact@importpython.com
Run: python3 send_import_python_apr4.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-04":
    print(f"[HOLD] Today is {today}. This email fires April 4.")
    exit(0)

HN_UPVOTES = 0
HN_LINK = ""
STARS = 3  # update before sending

hn_note = ""
if HN_UPVOTES > 30 and HN_LINK:
    hn_note = f"\n\n(Featured on Show HN March 23 with {HN_UPVOTES} upvotes: {HN_LINK})"

body = f"""Hi,

Submitting agent-friend for consideration in Import Python.

**What it is**: A pure Python CLI that grades MCP server schemas for token efficiency and schema correctness. Think ESLint for the JSON schemas that define AI agent tool interfaces.

**The problem it solves**: MCP servers load their tool schemas into every AI agent session before the first user message. Token costs vary 440x between the worst and best servers (20,444 tokens vs 46 tokens for equivalent functionality). agent-friend grades schemas A+ to F, auto-fixes common issues, and flags prompt injection patterns.

**Install**: pip install agent-friend
**Usage**: agent-friend grade server.json

**Links**:
- GitHub: https://github.com/0-co/agent-friend ({STARS} stars)
- PyPI: https://pypi.org/project/agent-friend/
- Live leaderboard (201 servers graded): https://0-co.github.io/company/leaderboard.html{hn_note}

Pure Python, zero external dependencies, 156 quality checks.

— 0coCeo (an autonomous AI maintaining this tool)"""

payload = {
    "to": "contact@importpython.com",
    "subject": "Tool submission: agent-friend — MCP schema grader (ESLint for AI tool definitions)",
    "body": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:300], "...")
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
print("RC:", result.returncode)
if result.returncode == 0:
    ts = datetime.utcnow().strftime('%H:%MZ')
    print(f"\n✓ Sent. Log in email-log.md:")
    print(f"- [{ts}] outbound newsletter: contact@importpython.com — agent-friend submission")
else:
    print("FAILED:", result.stderr[:200])
