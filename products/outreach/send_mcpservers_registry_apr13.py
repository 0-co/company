#!/usr/bin/env python3
"""
Send registry partnership email to mcpservers.org advertising team.
Scheduled: April 13, 2026
Goal: Get agent-friend grades displayed next to server listings.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-13":
    print(f"[HOLD] Today is {today}. This email fires April 13.")
    exit(0)

EMAIL_LOG = "/home/agent/company/email-log.md"

body = """Hi,

We're listed on mcpservers.org — thank you for including agent-friend.

We've been grading MCP servers for schema quality: 201 servers, A+ to F, 69 automated checks. We measure token cost, naming conventions, type safety, and schema completeness. Full leaderboard: https://0-co.github.io/company/leaderboard.html

Token costs vary 440x across servers (PostgreSQL: 46 tokens/tool, Desktop Commander: 4,192 tokens/tool). Developers browsing directories have no visibility into this.

Would mcpservers.org want to show quality grades next to server listings?

We'd provide a free JSON data feed: { server_name, grade, score, token_count } — no cost, just attribution. Developers would get a quality signal when choosing servers. You'd stand out from other directories.

We'd add a "featured on mcpservers.org" badge to our leaderboard in return.

Interested?

— 0coCeo
AI agent CEO, agent-friend maintainer
https://github.com/0-co/agent-friend
(Autonomous AI, building in public at twitch.tv/0coceo)"""

payload = {
    "to": "advertising@mcpservers.org",
    "subject": "Quality grades for your MCP server listings — data partnership",
    "text": body
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("RC:", result.returncode)
print("OUT:", result.stdout[:200])

if result.returncode == 0:
    ts = datetime.utcnow().strftime("%H:%MZ")
    with open(EMAIL_LOG, "a") as f:
        f.write(f"- [{ts}] outbound cold: advertising@mcpservers.org — subject \"Quality grades for your MCP server listings — data partnership\" — registry partnership pitch, H28\n")
    print("Logged to email-log.md")
