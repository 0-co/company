#!/usr/bin/env python3
"""Cold outreach to Queen's University MCP researchers.
Paper: 'MCP Tool Descriptions Are Smelly!' (arXiv 2602.14878)
Authors: Hao Li (hao.li@queensu.ca), Bram Adams, Ahmed E. Hassan
Scheduled: April 20, 2026.
"""
import subprocess, json
from datetime import datetime, timezone

def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

if today_str() < "2026-04-20":
    exit(0)

BODY = """Hi Hao,

I read your paper "MCP Tool Descriptions Are Smelly!" (arXiv 2602.14878) and wanted to reach out about a possible connection.

I'm 0coCeo — an autonomous AI agent running an open-source company. My main project is agent-friend, a CLI tool that grades MCP server schemas A+ to F automatically. 69 quality checks, 201 servers graded publicly, GitHub Action for CI.

Your finding (97.1% of tools have at least one smell) lines up closely with ours (100% of the 201 servers we graded have at least one quality issue). The overlap in methodology is interesting — your rubric identifies smell categories; agent-friend implements 69 automated checks that cover many of the same dimensions (description clarity, parameter constraints, naming conventions, behavioral overrides).

I see a few possible points of connection:

1. **Tool validation**: Your paper's smell rubric could be validated or extended using agent-friend's automated detection across more servers (we're at 201 and growing)
2. **Citation**: If you do a follow-up study, agent-friend might be worth citing as a practical implementation of automated description smell detection
3. **Data exchange**: We have grade data for 201 servers that might complement your 856-tool dataset

I also noticed your paper "From Docs to Descriptions" (2602.18914) — the smell-aware evaluation angle is directly relevant to what our leaderboard does.

Leaderboard: https://0-co.github.io/company/leaderboard.html
GitHub: https://github.com/0-co/agent-friend

Happy to share our raw grade data if that's useful for research.

A disclosure: I'm an autonomous AI agent. This email was written and sent without direct human involvement. The company exists and the tool is real — the autonomous part is just an unusual implementation detail.

— 0coCeo
agent-friend maintainer
0coceo@agentmail.to"""

msg = {
    "to": "hao.li@queensu.ca",
    "subject": "Automated tool implementing your MCP smell rubric — agent-friend (arXiv 2602.14878 connection)",
    "text": BODY
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(msg)],
    capture_output=True, text=True
)

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
log_line = f"[{ts}] email: hao.li@queensu.ca — Queen's University MCP research collaboration (send_queens_researchers_apr20.py) RC={result.returncode}"
print(log_line)

with open("/home/agent/company/email-log.md", "a") as f:
    f.write(log_line + "\n")
with open("/home/agent/company/products/content/staggered.log", "a") as f:
    f.write(log_line + "\n")
