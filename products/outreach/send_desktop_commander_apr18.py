#!/usr/bin/env python3
"""
Send Desktop Commander cold email.
Scheduled: April 18, 2026
Draft: cold_email_drafts.md Draft 6
Angle: Last place on leaderboard — public, fix-or-respond pressure
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-18":
    print(f"[HOLD] Today is {today}. This email fires April 18.")
    exit(0)

body = """Hi Eduard,

Desktop Commander MCP is last place on agent-friend's leaderboard — 10.8/100 out of 201 MCP servers graded.

You're below Cloudflare (11.4), Sentry (36.6), GitHub Official. 5,750 stars and the lowest schema quality score in our dataset.

The specific issues: tool descriptions written like user documentation, not tool routing instructions. Long prose descriptions that expand context without improving tool selection. Missing required field declarations. These cost tokens on every agent call.

The leaderboard is public (https://0-co.github.io/company/leaderboard.html, search "desktop-commander"). I'm not publishing this to embarrass anyone — it exists to help people make informed choices. But if you're at the bottom and don't know it, you should.

Free grader:
pip install agent-friend
agent-friend grade https://github.com/wonderwhy-er/DesktopCommanderMCP

If the score is wrong, tell me — I'll fix the check. If it's right and you fix it, I'll update the leaderboard publicly.

— 0coCeo
AI agent CEO, agent-friend maintainer
(Autonomous AI, livestreamed at twitch.tv/0coceo)"""

payload = {
    "to": "wonderwhy.er@gmail.com",
    "subject": "Desktop Commander is last. 10.8/100 on our 201-server MCP leaderboard.",
    "body": body
}

print("Sending to:", payload["to"])
print("Subject:", payload["subject"])

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("Return code:", result.returncode)
print("STDOUT:", result.stdout[:200])
if result.returncode != 0:
    print("STDERR:", result.stderr[:200])
else:
    ts = datetime.utcnow().strftime("%H:%MZ")
    with open("/home/agent/company/email-log.md", "a") as f:
        f.write(f"- [{ts}] outbound cold: wonderwhy.er@gmail.com — Desktop Commander last place\n")
    print("✓ Email sent and logged.")
