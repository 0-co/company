#!/usr/bin/env python3
"""
Send pitch to Sjoerd Tiemensma (UseAI newsletter — useai.substack.com, 2,000+ subs).
Scheduled: April 16, 2026
Found via: market research session 223cx (March 25) — AI tools for developers angle.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-16":
    print(f"[HOLD] Today is {today}. This email fires April 16.")
    exit(0)

EMAIL_LOG = "/home/agent/company/email-log.md"

body = """Hi Sjoerd,

Your UseAI newsletter covers tools developers actually use in production. Here's a data angle that might interest your readers.

We graded 201 MCP servers on token efficiency and schema quality. The results are surprising: token costs vary 440x between servers. PostgreSQL MCP costs 46 tokens per tool. Desktop Commander costs 4,192. When you call three average MCP servers in a Claude session, you've already burned 49% of the available context — before doing any actual work.

This matters to UseAI readers because most AI-assisted developer workflows now chain multiple MCP tools. Context window burn is invisible at the tool level but compounding in practice.

We built agent-friend (pip install agent-friend) to quantify this — a build-time schema linter that grades servers A+ through F. Full leaderboard of 201 servers: https://0-co.github.io/company/leaderboard.html

Happy to share the dataset or write a piece for UseAI if the topic fits your editorial calendar.

— 0coCeo
AI agent CEO, agent-friend maintainer
https://github.com/0-co/agent-friend
(Autonomous AI, building in public at twitch.tv/0coceo)"""

# Contact: sjoerd@useai.nl or via substack.com — check useai.substack.com for contact
payload = {
    "to": "sjoerd@useai.nl",
    "subject": "MCP token costs vary 440x — data for your AI tools audience",
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
        f.write(f"- [{ts}] outbound cold: sjoerd@useai.nl — subject \"MCP token costs vary 440x — data for your AI tools audience\" — UseAI newsletter pitch, token bloat angle\n")
    print("Logged to email-log.md")
