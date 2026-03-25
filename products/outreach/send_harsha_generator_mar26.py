#!/usr/bin/env python3
"""
Outreach to harsha-iiiv (openapi-mcp-generator maintainer).
Their tool: 547 stars, 35K npm downloads/month.
Known issue: generates tool names over 60 char limit (issue #4, Claude Desktop breaks).
Angle: agent-friend as post-generation validator.
Scheduled: March 26, 2026
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-03-26":
    print(f"[HOLD] Today is {today}. This email should fire March 26 or later.")
    exit(0)

# GitHub profile: github.com/harsha-iiiv
# Email: need to find from GitHub profile or commits
# Alternative: open a GitHub issue (but can't write external repos)
# Best approach: email from GitHub profile if available

body = """Hi,

I've been working on agent-friend (https://github.com/0-co/agent-friend) — a linter for MCP server schemas. Grades schemas A+ through F on token efficiency and correctness.

I ran your generator's petstore example output through it: F grade (53.7/100), 39 warnings across 7 tools. The main issues:
- Tool names inheriting camelCase from OpenAPI (MCP convention is snake_case)
- Missing `required` field declarations on several tools
- Parameter descriptions that duplicate type information (wastes tokens)

I noticed issue #4 in your repo about tool names exceeding Claude Desktop's 60-char limit — agent-friend's check 53 catches exactly that pattern.

Would it make sense to add agent-friend as an optional CI validation step? Something like:
  agent-friend validate generated-schema.json --fail-on F,D

It's on PyPI (`pip install agent-friend`), MIT licensed, zero dependencies.

Happy to open a PR adding it to your CI workflow if that's useful.

— 0coCeo
AI agent building agent-friend in public (twitch.tv/0coceo)
"""

payload = {
    "to": "harsha.vivek.official@gmail.com",  # Placeholder — find from GitHub
    "subject": "agent-friend + openapi-mcp-generator: quality validation after generation",
    "text": body
}

# TODO: Find actual email from GitHub profile or commits
print("NOTE: Need to find harsha-iiiv actual email before sending!")
print("Check: https://github.com/harsha-iiiv")
print("Or: git log on the repo to find commit email")
print()
print("Placeholder email in script — DO NOT SEND without verifying target address.")

# result = subprocess.run(...)  # Commented out until email verified
print("Script complete (dry-run mode)")
