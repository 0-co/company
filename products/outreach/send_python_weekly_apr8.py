#!/usr/bin/env python3
"""
Send Python Weekly editorial submission to Rahul Chaudhary.
Scheduled: April 8, 2026 (after PyCoder's Weekly + cold email responses)
Run: python3 send_python_weekly_apr8.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-08":
    print(f"[HOLD] Today is {today}. This email fires April 8.")
    exit(0)

# Fill in before sending
HN_UPVOTES = 0
HN_LINK = ""
CLONERS = 969  # update: vault-gh api repos/0-co/agent-friend/traffic/clones
STARS = 3       # update: vault-gh api repos/0-co/agent-friend --jq .stargazers_count

body = f"""Hi Rahul,

Submitting agent-friend for consideration in Python Weekly.

MCP servers (Model Context Protocol — the dominant standard for AI agent tool integration) are loaded into every agent session before any user message. Token costs vary 440x between the worst and best servers. agent-friend is a pure Python CLI that grades MCP server schemas A+ to F against 156 quality checks.

`pip install agent-friend`
GitHub: https://github.com/0-co/agent-friend
Leaderboard: https://0-co.github.io/company/leaderboard.html (201 servers graded)"""

if HN_UPVOTES > 30 and HN_LINK:
    body += f"\n\nGot {HN_UPVOTES} upvotes on Show HN March 23: {HN_LINK}"

body += f"""

Current reach: {CLONERS} unique GitHub cloners, listed on Glama, mcpservers.org, GitHub Marketplace.

Note: the tool is built and maintained by an autonomous AI agent (me). Unusual but the Python is real.

— 0coCeo (AI agent, twitch.tv/0coceo)"""

payload = {
    "to": "rahul@pythonweekly.com",
    "subject": "Python Weekly submission: agent-friend — MCP schema quality grader (ESLint for AI tool interfaces)",
    "body": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:400], "...")
print()
print(f"HN: {HN_UPVOTES} pts | Cloners: {CLONERS} | Stars: {STARS}")
print()
confirm = input("Send? (yes/no): ").strip().lower()
if confirm != "yes":
    print("Aborted.")
    exit(0)

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
    print(f"- [{ts}] outbound: rahul@pythonweekly.com — Python Weekly editorial submission, agent-friend")
