#!/usr/bin/env python3
"""
Send partnership email to Stephan Fitzpatrick (mcp2cli author).
Scheduled: April 16, 2026
Angle: Complementary tools — runtime (mcp2cli) + build-time (agent-friend).
mcp2cli got 158 HN points in March 2026.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-16":
    print(f"[HOLD] Today is {today}. This email fires April 16.")
    exit(0)

EMAIL_LOG = "/home/agent/company/email-log.md"

body = """Hi Stephan,

mcp2cli is the cleanest approach to the runtime bloat problem I've seen — and the 158 HN points confirmed the pain is real.

We're working on the complementary build-time layer: agent-friend grades MCP server schemas for quality (A+ to F, 69 checks, 201 servers). Token cost varies 440x across servers. Fixing source schemas means mcp2cli has less to strip AND schemas work better in clients that don't use mcp2cli.

The framing that resonates: "mcp2cli for when you can't change the server; agent-friend for when you can."

Two questions:

1. Would it make sense to mention agent-friend in mcp2cli's README as a "build-time complement"? We'd do the same for agent-friend → mcp2cli. Both audiences benefit from knowing both tools exist.

2. Do you see anything in the mcp2cli usage data that would be useful for the schema quality side? You're generating schemas at runtime — we grade them at build time. There might be interesting overlap in the failure patterns.

Full grading tool (free): https://github.com/0-co/agent-friend

— 0coCeo
AI agent CEO, agent-friend maintainer
(Autonomous AI, building in public at twitch.tv/0coceo)"""

payload = {
    "to": "stephan@knowsuchagency.com",
    "subject": "mcp2cli + agent-friend: complementary tools for the same problem",
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
        f.write(f"- [{ts}] outbound cold: stephan@knowsuchagency.com — subject \"mcp2cli + agent-friend: complementary tools\" — partnership pitch, mcp2cli 158pt HN\n")
    print("Logged to email-log.md")
