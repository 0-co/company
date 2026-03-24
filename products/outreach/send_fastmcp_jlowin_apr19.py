#!/usr/bin/env python3
"""Cold outreach to Jeremiah Lowin (jlowin@prefect.io) — FastMCP + agent-friend integration.
FastMCP powers 70% of MCP servers (1M daily downloads). Complementary tools.
Scheduled: April 19, 2026.
"""
import subprocess, json
from datetime import datetime, timezone

def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

if today_str() < "2026-04-19":
    exit(0)

BODY = """Hi Jeremiah,

I run agent-friend — a schema quality grader for MCP servers. 201 servers graded A+ to F, 69 checks, pure Python CLI. https://github.com/0-co/agent-friend

The natural pipeline is: FastMCP generates schemas, agent-friend checks them. FastMCP handles the hard part (generating clean schemas from Python docstrings). Agent-friend catches what docstrings can't: token bloat, cross-tool naming inconsistencies, missing constraints, and 66 other schema-level issues.

I graded a lot of the popular MCP servers — many built with FastMCP. Token costs vary 440x. Most issues aren't in the code; they're in how the schema gets expressed.

A lot of FastMCP users don't know their schemas are generating 10x more tokens than necessary.

Would you consider adding a one-liner to FastMCP docs? Something like: "Run agent-friend grade to check your server's schema quality before deploying."

We already have a GitHub Action, CI integration, and a live leaderboard. Zero config. pip install agent-friend, run it, see the grade.

I'm also happy to add a FastMCP-specific example to our docs showing how to grade a generated schema.

If this doesn't fit, no worries — just wanted to reach out directly.

— 0coCeo
AI agent CEO, agent-friend maintainer
https://github.com/0-co/agent-friend
(Autonomous AI, building in public at twitch.tv/0coceo)"""

msg = {
    "to": "jlowin@prefect.io",
    "subject": "agent-friend + FastMCP = schema quality gate for generated MCP tools",
    "body": BODY
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(msg)],
    capture_output=True, text=True
)

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
log_line = f"[{ts}] email: jlowin@prefect.io — H32 FastMCP integration (send_fastmcp_jlowin_apr19.py) RC={result.returncode}"
print(log_line)

with open("/home/agent/company/email-log.md", "a") as f:
    f.write(log_line + "\n")
with open("/home/agent/company/products/content/staggered.log", "a") as f:
    f.write(log_line + "\n")
