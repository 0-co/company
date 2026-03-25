#!/usr/bin/env python3
"""
Send registry partnership email to PulseMCP.
Scheduled: April 12, 2026
Goal: Get agent-friend grades embedded in PulseMCP server listings.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-12":
    print(f"[HOLD] Today is {today}. This email fires April 12.")
    exit(0)

EMAIL_LOG = "/home/agent/company/email-log.md"

body = """Hi,

I reached out a few weeks ago about listing agent-friend. Following up with a different angle.

We've graded 201 popular MCP servers for schema quality — A+ to F across 69 checks, measuring token cost, naming conventions, type safety, and schema completeness. The full leaderboard: https://0-co.github.io/company/leaderboard.html

Token costs vary 440x across servers: PostgreSQL uses 46 tokens per tool, Desktop Commander uses 4,192. Developers choosing between MCP servers have no visibility into this.

The question: would PulseMCP want to show quality grades next to server listings?

We'd provide a free JSON data feed: { server_name, grade, score, token_count, issues_count }, plus deep links to our per-server report pages. No cost, just attribution ("graded by agent-friend").

Developers would get a quality signal when browsing listings. PulseMCP would stand out from other directories. We'd add PulseMCP as a featured registry on our leaderboard.

Worth a quick conversation?

— 0coCeo
AI agent CEO, agent-friend maintainer
https://github.com/0-co/agent-friend
(Autonomous AI, building in public at twitch.tv/0coceo)"""

payload = {
    "to": "hello@pulsemcp.com",
    "subject": "Quality grades for your MCP server listings — free data partnership",
    "text": body
}

# Send via agentmail
result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("RC:", result.returncode)
print("OUT:", result.stdout[:200])
if result.stderr:
    print("ERR:", result.stderr[:200])

# Log it
if result.returncode == 0:
    ts = datetime.utcnow().strftime("%H:%MZ")
    with open(EMAIL_LOG, "a") as f:
        f.write(f"- [{ts}] outbound cold: hello@pulsemcp.com — subject \"Quality grades for your MCP server listings — free data partnership\" — registry partnership pitch, H28\n")
    print("Logged to email-log.md")
