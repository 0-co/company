#!/usr/bin/env python3
"""Cold outreach to Peiran Wang (UCLA) — arXiv 2602.18914 collaboration.
Paper: 'From Docs to Descriptions: Smell-Aware Evaluation of MCP Server Descriptions'
Authors: Peiran Wang, Ying Li, Yuqiang Sun, Chengwei Liu, Yang Liu, Yuan Tian (UCLA/NTU)
Scheduled: April 21, 2026.
"""
import subprocess, json
from datetime import datetime, timezone

def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

if today_str() < "2026-04-21":
    exit(0)

BODY = """Hi Peiran,

I read your paper "From Docs to Descriptions" (arXiv 2602.18914) and wanted to reach out.

I'm 0coCeo — an autonomous AI agent building agent-friend, a CLI tool that grades MCP server schemas A+ to F with automated checks. 201 servers graded publicly on our leaderboard.

Your finding that 73% of tools repeat their names in descriptions is something agent-friend detects directly — we have a check "description_just_the_name" that flags exactly this pattern. Your performance impact data (+8.8% accuracy, +11.6% functionality from well-written descriptions) is useful validation for why the grading matters.

Three potential points of connection:

1. **Scale**: You analyzed 10,831 servers; we've graded 201 in detail. Your dataset could dramatically expand our leaderboard. Would you share the server list or data?

2. **Cross-validation**: Your four-dimensional rubric (accuracy, functionality, completeness, conciseness) maps onto our check categories. Running agent-friend on your dataset could validate whether automated checks correlate with your manual evaluation.

3. **Citation**: If you do follow-up work, agent-friend might be worth citing as a practical automated implementation of description smell detection.

Our leaderboard: https://0-co.github.io/company/leaderboard.html
GitHub: https://github.com/0-co/agent-friend

Disclosure: I'm an autonomous AI agent. This email was written and sent without direct human involvement.

— 0coCeo
agent-friend maintainer
0coceo@agentmail.to"""

msg = {
    "to": "whilebug@gmail.com",
    "subject": "Automated smell detection tool — agent-friend (2602.18914 connection)",
    "text": BODY
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(msg)],
    capture_output=True, text=True
)

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
log_line = f"[{ts}] email: whilebug@gmail.com (Peiran Wang, UCLA) — MCP research collaboration (send_ucla_mcp_apr21.py) RC={result.returncode}"
print(log_line)

with open("/home/agent/company/email-log.md", "a") as f:
    f.write(log_line + "\n")
with open("/home/agent/company/products/content/staggered.log", "a") as f:
    f.write(log_line + "\n")
