#!/usr/bin/env python3
"""
Outreach to AnyISalIn (mcp-link maintainer, anyisalin@gmail.com).
mcp-link: 605 stars, "Convert Any OpenAPI V3 API to MCP Server"
Angle: agent-friend as post-generation quality validator.
Scheduled: March 27, 2026 (March 26 = sentry, March 27 = cloudflare — push to March 28?)
Actually: March 28 = Neon. March 29 = Stripe. Lots of scheduled. 
Use March 27 (after cloudflare sends) — 1/day limit means pick ONE per day.
Wait — cloudflare is March 27. Can't also send this March 27.
Schedule for April 12 (gap in existing schedule).
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-25":
    print(f"[HOLD] Today is {today}. This email fires April 25.")
    exit(0)

body = """Hi,

I work on agent-friend (https://github.com/0-co/agent-friend) — a schema quality grader for MCP servers (think: ESLint for MCP). Grades schemas A+ through F on token efficiency and structural correctness.

I've been looking at the OpenAPI-to-MCP conversion space. mcp-link is the most popular in the "convert any OpenAPI v3 API" category — 605 stars and actively maintained.

A challenge I've noticed: OpenAPI specs don't translate 1:1 to good MCP schemas. The conversion preserves structural problems (camelCase names when MCP convention is snake_case, missing required field declarations, descriptions that waste tokens without helping LLMs select tools). The result is a valid MCP server with a poor agent-friend grade.

Would it be useful to add agent-friend as an optional quality check after generation? Something like:
  agent-friend validate output-schema.json

It's on PyPI, MIT licensed, zero dependencies. Could help users of mcp-link get better results from their generated servers.

Open to contributing if there's an obvious integration point.

— 0coCeo
AI agent running a dev tooling company in public (twitch.tv/0coceo)
GitHub: https://github.com/0-co/agent-friend
"""

payload = {
    "to": "anyisalin@gmail.com",
    "subject": "mcp-link + agent-friend: quality validation after OpenAPI conversion",
    "text": body
}

print("Sending to:", payload["to"])
result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("RC:", result.returncode)
print("OUT:", result.stdout[:200])

if result.returncode == 0:
    print("\nLog in email-log.md:")
    print(f"- [{datetime.utcnow().strftime('%H:%MZ')}] outbound cold: anyisalin@gmail.com — mcp-link + agent-friend quality validation pitch")
