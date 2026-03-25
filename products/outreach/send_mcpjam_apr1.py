#!/usr/bin/env python3
"""Cold outreach to MCPJam newsletter (matthew@mcpjam.com).
MCPJam = "Postman for MCP" inspector tool, 1,816 stars, ~700 subscriber newsletter.
angle: MCPJam covers dev tools for testing MCP servers. agent-friend does
build-time schema quality grading. complementary, not competitive.
they covered "5 MCP dev tools for server testing" — we weren't in it.
"""
import subprocess, json, sys
from datetime import date

SEND_DATE = "2026-04-01"
INBOX = "0coceo@agentmail.to"
TO = "matthew@mcpjam.com"
SUBJECT = "agent-friend grades 201 MCP servers for token bloat — worth covering in MCPJam newsletter?"

BODY = """Hi Matthew,

Big fan of MCPJam Inspector — you've built the best MCP debugging tool in the ecosystem. The "5 MCP dev tools" newsletter piece was great.

One tool you might have missed: agent-friend (github.com/0-co/agent-friend). We grade MCP server schemas for token efficiency and quality — think ESLint meets CI for MCP. We've graded 201 servers publicly at https://0-co.github.io/company/leaderboard.html.

Some findings that might interest your readers:
- Token costs vary 440x across 201 servers (46 tokens vs 20,444 tokens)
- Context7 (50K GitHub stars, #1 MCP server): 7.5/100. F grade.
- GitHub official MCP: 20,444 tokens. Grade F.
- PostgreSQL: 46 tokens, 1 tool. A+.

MCPJam = runtime testing/inspection. agent-friend = build-time quality grading. They address different parts of the MCP developer workflow. Together: lint before you ship, debug after.

Worth a mention in your next "MCP dev tools" roundup?

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
    "text": BODY
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", f"/inboxes/{INBOX}/messages/send", json.dumps(payload)],
    capture_output=True, text=True
)

if result.returncode == 0:
    print(f"Sent MCPJam outreach to {TO}")
else:
    print(f"FAILED: {result.stderr[:200]}")
    sys.exit(1)
