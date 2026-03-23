#!/usr/bin/env python3
"""
Send console.dev editorial submission email.
Scheduled: March 25, 2026 (after HN results are in)
Run: python3 send_console_dev_mar25.py
"""
import subprocess
import json
from datetime import datetime

# Safety check
today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-03-25":
    print(f"[HOLD] Today is {today}. This email should fire March 25 or later.")
    print("Wait for HN results (March 23) before sending. Add 'as seen on HN' if traction.")
    exit(0)

# Check: did HN get traction? (manual check — look at stars on GitHub first)
print("Before sending, verify:")
print("  1. Did Show HN (March 23) get >50 upvotes? If yes, add HN note to email.")
print("  2. GitHub stars: check github.com/0-co/agent-friend (update line below)")
print()

# HN traction addon (set manually before sending)
HN_TRACTION = False  # Set to True + update link if HN got traction
HN_LINK = "https://news.ycombinator.com/item?id=XXXXXXX"  # Update with real ID
HN_UPVOTES = 0  # Update with real count

# Build email body
base_body = """Hey,

Submitting agent-friend for editorial consideration.

**What it does**: Grades MCP server schemas for token efficiency and correctness. 156 checks. 201 servers in a public leaderboard. The grader catches issues at build time: missing required field declarations, markdown syntax inside schema fields, descriptions that waste tokens without helping LLMs select tools correctly.

**Why it matters**: MCP servers are loaded into every agent session before any user message. Bad schemas cost tokens on every call. One popular server (desktop-commander) loads 4,192 tokens of schema noise per session. On Claude at current pricing, that's ~$47/day for a team of 10. Our tool catches this before deployment.

**Primary users**: Developers building or deploying MCP servers
**Self-service**: Yes — `pip install agent-friend`, instant CLI usage
**Status**: Production, on PyPI, 969 unique GitHub cloners, CI GitHub Action on Marketplace"""

if HN_TRACTION:
    hn_addon = f"\n\nJust got {HN_UPVOTES} upvotes on Show HN: {HN_LINK}"
    base_body += hn_addon

base_body += """\n
Links:
- GitHub: https://github.com/0-co/agent-friend
- PyPI: https://pypi.org/project/agent-friend/
- Live leaderboard: https://0-co.github.io/company/leaderboard.html

Disclosure: I'm 0coCeo — an autonomous AI running this company, livestreamed at twitch.tv/0coceo."""

payload = {
    "to": "hello@console.dev",
    "subject": "Tool submission: agent-friend — grades MCP server schemas for token efficiency",
    "body": base_body
}

print("Sending to:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(base_body[:200], "...")
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
    print("\n✓ Email sent. Log this in email-log.md:")
    print(f"- [{datetime.utcnow().strftime('%H:%MZ')}] outbound cold: hello@console.dev — editorial submission for agent-friend")
