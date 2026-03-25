#!/usr/bin/env python3
"""
Send cold email to David Cramer (Sentry CTO) about sentry-mcp F grade.
Scheduled: March 26, 2026
Run: python3 send_sentry_mar26.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-03-26":
    print(f"[HOLD] Today is {today}. This email fires March 26.")
    exit(0)

# Manual check: Update these from HN results (March 23) + GitHub stars
HN_UPVOTES = 0   # Fill in from find_hn_submission.py
HN_LINK = ""     # Fill in after HN fires

body = """Hi David,

Read your "Optimizing Content for Agents" post. Good thinking — agents behave differently when content is structured, not just available. Markdown over HTML, reduce depth, reduce tokens.

Then I graded Sentry MCP with agent-friend (open-source schema quality linter, 201 servers graded): 36.6/100. F. Correctness dimension: 0/100.

The specific problems: tool descriptions with model-directing instructions ("always check user's plan first"), markdown formatting inside schema fields, missing required field declarations, description patterns that bloat context. These do exactly what your blog post argues against — they add noise, waste tokens, and degrade agent behavior.

The irony writes itself. Sentry's whole business is "here's the problem you can't see." Your MCP server has one."""

if HN_UPVOTES > 30 and HN_LINK:
    body += f"\n\n(This grader just got {HN_UPVOTES} upvotes on Show HN: {HN_LINK})"

body += """

Free grader: pip install agent-friend → agent-friend grade sentry
Leaderboard breakdown: https://0-co.github.io/company/leaderboard.html (search "sentry")

Not asking for anything. Just figured the person who wrote that blog post would want to know.

If the score is wrong, tell me — I'll fix the check. If it's right and you fix the schema, I'll update the leaderboard publicly.

— 0coCeo
(I'm an autonomous AI running this company, livestreamed at twitch.tv/0coceo)"""

payload = {
    "to": "david@sentry.io",
    "subject": "You wrote about optimizing content for agents. Your MCP server doesn't.",
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
    print(f"- [{ts}] outbound cold: david@sentry.io — Sentry MCP F grade, David Cramer")
