#!/usr/bin/env python3
"""Cold outreach to Stacklok (hello@stacklok.com).
Stacklok ToolHive = runtime MCP token optimizer, 1.7K stars, enterprise-grade.
Angle: we're build-time quality grading, they're runtime filtering. Complementary.
Our leaderboard shows WHY a server is bloated; their tool fixes it at runtime.
"""
import subprocess, json, sys
from datetime import date

SEND_DATE = "2026-04-10"
INBOX = "0coceo@agentmail.to"
TO = "hello@stacklok.com"
SUBJECT = "Our leaderboard shows WHY MCP servers are bloated — might pair well with ToolHive"

BODY = """Hi Stacklok team,

Big fan of ToolHive MCP Optimizer — runtime filtering is the right approach for teams already deployed.

We built a complementary build-time layer: agent-friend grades MCP server schemas A+ through F for token efficiency and schema quality (github.com/0-co/agent-friend). We've graded 201 public servers at https://0-co.github.io/company/leaderboard.html.

The pairing is natural:
- agent-friend: shows you the root cause (a 2,006-char description, missing types, 106 tools)
- ToolHive: filters at runtime to reduce token spend per request

Your "54,600 tokens burned on init" example maps directly to what we grade. Context7 (50K stars, most popular MCP server): 7.5/100 on our schema quality grader, F grade.

Might be worth mentioning the build-time / runtime distinction in your blog or docs? Happy to share our leaderboard data.

— 0coCeo
0coCeo (claude-sonnet-4-6 instance, building https://github.com/0-co/agent-friend)
"""

def today_str():
    return date.today().isoformat()

if today_str() < SEND_DATE:
    print(f"Not yet {SEND_DATE}, exiting")
    sys.exit(0)

payload = {
    "to": TO,
    "subject": SUBJECT,
    "body": BODY
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", f"/inboxes/{INBOX}/messages/send", json.dumps(payload)],
    capture_output=True, text=True
)

if result.returncode == 0:
    print(f"Sent Stacklok outreach to {TO}")
else:
    print(f"FAILED: {result.stderr[:200]}")
    sys.exit(1)
