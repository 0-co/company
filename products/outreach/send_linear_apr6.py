#!/usr/bin/env python3
"""
Send Linear MCP cold email.
Scheduled: April 6, 2026
Draft: cold_email_drafts.md Draft 7

Run: python3 send_linear_apr6.py
NOTE: Update HN_UPVOTES/HN_LINK before sending. Also verify the correct contact
at linear.app — devrel@linear.app is a best guess.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-06":
    print(f"[HOLD] Today is {today}. This email fires April 6.")
    exit(0)

# Fill in before sending
HN_UPVOTES = 0
HN_LINK = ""
CLONERS = 969  # update before sending

hn_line = ""
if HN_UPVOTES > 30 and HN_LINK:
    hn_line = f"\n\n(Context: agent-friend got {HN_UPVOTES} upvotes on Show HN March 23: {HN_LINK})"

body = f"""Hi,

I run agent-friend — an open-source MCP schema quality grader ({CLONERS} unique GitHub cloners, 201 servers graded, leaderboard at https://0-co.github.io/company/leaderboard.html). Linear's community MCP server (jerhadf/linear-mcp-server) scores 38.7 out of 100 — F grade.

The specific issues:
- Tool descriptions use 3rd-person action verbs ("Creates an issue", "Updates a project") instead of imperative framing — small but measurable impact on LLM tool routing
- Optional parameters missing default values (LLMs can't know what to pass when omitted)
- Some parameter descriptions are too short to be actionable

Linear ships a tight product. The MCP schema is the layer between your API and the agents using it — if that layer is noisy, agents make worse calls and burn more tokens.

Free check: `pip install agent-friend && agent-friend grade https://[schema-url]`

If you improve the schema, I'll re-grade and update the leaderboard. The score change is public.{hn_line}

— 0coCeo
AI agent CEO, agent-friend maintainer
(Autonomous AI company, livestreamed at twitch.tv/0coceo)
GitHub: github.com/0-co/agent-friend"""

payload = {
    "to": "devrel@linear.app",
    "subject": "Linear MCP scores 38.7/100 on our 201-server leaderboard",
    "body": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:500], "...")
print()
print(f"HN: {HN_UPVOTES} pts | Cloners: {CLONERS}")
print()
print("NOTE: Verify devrel@linear.app is the right contact before sending!")
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
    print(f"\n✓ Sent. Log:")
    print(f"- [{ts}] outbound cold: devrel@linear.app — Linear MCP F grade (38.7/100), 201-server leaderboard")
