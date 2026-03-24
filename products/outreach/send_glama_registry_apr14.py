#!/usr/bin/env python3
"""
Send registry partnership email to Glama.
Scheduled: April 14, 2026
Goal: Get agent-friend grades embedded in Glama MCP server listings.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-14":
    print(f"[HOLD] Today is {today}. This email fires April 14.")
    exit(0)

EMAIL_LOG = "/home/agent/company/email-log.md"

body = """Hi,

Our MCP server (agent-friend) is listed on Glama: https://glama.ai/mcp/servers/@0-co/agent-friend

Following up with a different angle. We've graded 201 popular MCP servers for schema quality — A+ to F across 69 checks, measuring token cost, naming quality, type safety. Full leaderboard: https://0-co.github.io/company/leaderboard.html

Token costs vary 440x: PostgreSQL at 46 tokens/tool vs Desktop Commander at 4,192. Developers choosing between servers on Glama don't see this.

Would Glama be interested in showing quality grades next to server listings?

We'd provide a free data feed. No integration required — even a link to our per-server report would help developers. We'd add a "graded on Glama" badge to our leaderboard.

Alternatively, if there's a Discord channel or partnership process, happy to discuss there.

— 0coCeo
AI agent CEO, agent-friend maintainer
https://github.com/0-co/agent-friend
(Autonomous AI, building in public at twitch.tv/0coceo)"""

payload = {
    "to": "support@glama.ai",
    "subject": "Partnership proposal: quality grades for Glama server listings",
    "body": body
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
        f.write(f"- [{ts}] outbound cold: support@glama.ai — subject \"Partnership proposal: quality grades for Glama server listings\" — registry partnership pitch, H28\n")
    print("Logged to email-log.md")
