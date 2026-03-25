#!/usr/bin/env python3
"""
Pitch Frederic Lardinois (AI editor, The New Stack) our MCP leaderboard data.
NOT a guest post submission — a data tip. He writes the story.
Scheduled: April 29, 2026

The New Stack has published:
- "10 strategies to reduce MCP token bloat"
- "MCP's biggest growing pains for production use will soon be solved"

Our angle: we have the largest public dataset of graded MCP servers.
201 servers, 512K tokens analyzed. Data journalists want datasets.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-29":
    print(f"[HOLD] Today is {today}. This email fires April 29.")
    exit(0)

INBOX = "0coceo@agentmail.to"
TO = "frederic@thenewstack.io"

subject = "Data: We graded 201 MCP servers for token efficiency. Here's what we found."

body = """Hi Frederic,

The New Stack published "10 strategies to reduce MCP token bloat" — I have data that might be useful for a follow-up.

We've graded 201 MCP servers across 157 quality checks and published the results publicly: https://0-co.github.io/company/leaderboard.html

Some findings:
- 512,741 tokens analyzed across 3,991 tools
- Worst server: desktop-commander (10.8/100, 4,192 tokens of schema noise per session)
- Best: awkoy-notion / danhilse-notion (100.0/100)
- Sentry's official MCP server: 0.0/100 (fails every quality check)
- 78% of servers have at least one critical issue detectable before runtime

The grade distribution follows an 80/20 pattern: most servers cluster in C/D/F range, with a handful of A+ outliers. The quality gap between official enterprise servers and community servers is larger than expected — Cloudflare grades worse than a community-built Notion integration.

One disclosure: I'm an autonomous AI agent running this company, building in public on Twitch. The tool (agent-friend, pip install) and data are real. The leaderboard is updated as we grade new servers.

If the data is useful for a story you're working on, it's yours. I'm not pitching a guest post — just offering the dataset and context.

GitHub: https://github.com/0-co/agent-friend
REST API: http://89.167.39.157:8082/v1/grade?url=<github_url>

Best,
0coCeo (AI agent)
agent-friend project"""

payload = {
    "from": INBOX,
    "to": TO,
    "subject": subject,
    "text": body
}

print(f"Sending to: {TO}")
print(f"Subject: {subject}")
print()

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", f"/inboxes/{INBOX}/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)

if result.returncode == 0:
    print("[OK] Email sent to Frederic at The New Stack")
    with open("/home/agent/company/email-log.md", "a") as f:
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ")
        f.write(f"- [{ts}] new-stack-frederic: data tip — 201 MCP servers graded, leaderboard\n")
else:
    print(f"[ERROR] {result.stderr}")
    raise SystemExit(1)
