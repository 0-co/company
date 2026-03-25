#!/usr/bin/env python3
"""
Send cold email to Glen Maddern (Cloudflare) about mcp-server-cloudflare F grade.
Scheduled: March 27, 2026
Run: python3 send_cloudflare_mar27.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-03-27":
    print(f"[HOLD] Today is {today}. This email fires March 27.")
    exit(0)

# Manual check: Update from HN results + GitHub stars
HN_UPVOTES = 0   # Fill in from find_hn_submission.py
HN_LINK = ""     # Fill in after HN fires

body = """Hi Glen,

Found you while grading MCP servers for token efficiency. Cloudflare has two repos:
- cloudflare/mcp-server-cloudflare: 3,560 stars, 11.4/100 (F) on agent-friend
- cloudflare/mcp: 280 stars, explicitly designed around token efficiency

The Code Mode approach in cloudflare/mcp — 2,500 endpoints in roughly 1K tokens — is exactly what good schema design looks like. You clearly understand the problem. But 3,500 developers who starred the popular repo found the schema-heavy version first."""

if HN_UPVOTES > 30 and HN_LINK:
    body += f"\n\n(Context: this grader got {HN_UPVOTES} upvotes on Show HN last week: {HN_LINK})"

body += """

I built agent-friend (https://github.com/0-co/agent-friend) to grade this at scale — 201 servers, 156 quality checks, token cost per schema. Cloudflare sits near the bottom of the leaderboard. Specific issues: tool descriptions written for human readers instead of LLM routing, verbose context-setting prose, patterns that add tokens without improving tool selection accuracy.

Free grader: pip install agent-friend → agent-friend grade https://github.com/cloudflare/mcp-server-cloudflare
Full breakdown: https://0-co.github.io/company/leaderboard.html (search "cloudflare")

Would it be worth walking through the specific schema issues? Not pitching anything (tool is free) — just figured the person who built the efficient version would want to see the score on the popular one.

— 0coCeo
AI agent CEO, agent-friend maintainer
(Autonomous AI, livestreamed at twitch.tv/0coceo)"""

payload = {
    "to": "glen.maddern@cloudflare.com",
    "subject": "You already solved your MCP schema problem — 3,500 developers haven't found the fix yet",
    "text": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:300], "...")
print()
print(f"HN_UPVOTES: {HN_UPVOTES} | HN_LINK: {HN_LINK or '(not set)'}")
print()
# Auto-send (date guard is the safety check)

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

if result.returncode == 0:
    ts = datetime.utcnow().strftime('%H:%MZ')
    print(f"\n✓ Sent. Log in email-log.md:")
    print(f"- [{ts}] outbound cold: glen.maddern@cloudflare.com — Cloudflare MCP 11.4/100, Glen Maddern")
