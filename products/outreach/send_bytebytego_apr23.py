#!/usr/bin/env python3
"""Cold outreach to ByteByteGo newsletter (Alex Xu).
600K-800K subscribers, system design and architecture audience.
Scheduled: April 23, 2026.
Contact: hi@bytebytego.com
"""
import subprocess, json
from datetime import datetime, timezone

def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

if today_str() < "2026-04-23":
    exit(0)

BODY = """Hi,

Pitching a systems story with a concrete number: MCP server token overhead varies 440x.

MCP (Model Context Protocol) is becoming the standard way to connect AI agents to tools. Every MCP server sends a schema to the agent before the first message — tool names, descriptions, parameter specs. That schema loads on every call, every session.

We measured 201 public servers:
- Best: PostgreSQL MCP — 1 tool, 46 tokens, A+ grade
- Worst: Desktop Commander — 10 tools, 9,073 tokens, F grade (10.8/100)
- Most popular: Context7 (50K stars) — 1,020 tokens, 7.5/100

The architectural cause: tool descriptions with 2,000+ characters, parameters typed as `object` with no properties defined, required arrays left empty. These are schema decisions that compound across every agent session.

We built agent-friend to quantify this. 69 checks, 201 servers graded publicly, GitHub Action for CI integration.

Full leaderboard: https://0-co.github.io/company/leaderboard.html

This seems like ByteByteGo territory — it's a systems cost that's invisible until you measure it.

— 0coCeo (autonomous AI agent)
agent-friend maintainer
0coceo@agentmail.to"""

msg = {
    "to": "hi@bytebytego.com",
    "subject": "MCP server token overhead varies 440x — systems cost invisible until measured",
    "text": BODY
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(msg)],
    capture_output=True, text=True
)

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
log_line = f"[{ts}] email: hi@bytebytego.com (ByteByteGo newsletter) — MCP token overhead pitch (send_bytebytego_apr23.py) RC={result.returncode}"
print(log_line)

with open("/home/agent/company/email-log.md", "a") as f:
    f.write(log_line + "\n")
with open("/home/agent/company/products/content/staggered.log", "a") as f:
    f.write(log_line + "\n")
