#!/usr/bin/env python3
"""
Send PyCoder's Weekly link submission.
Scheduled: March 30, 2026
Run: python3 send_pycoders_weekly_mar30.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-03-30":
    print(f"[HOLD] Today is {today}. This email fires March 30.")
    exit(0)

# Update with HN results before sending
payload = {
    "to": "admin@pycoders.com",
    "subject": "Link submission: agent-friend — MCP schema linter / token cost analyzer",
    "text": """Hi,

Link submission for PyCoder's Weekly.

**agent-friend** — Static analyzer for MCP server schemas. 156 checks, 201 public servers graded (leaderboard), finds token bloat and schema correctness issues before deployment.

MCP (Model Context Protocol) is the dominant standard for connecting AI agents to tools (97M monthly SDK downloads). The schema quality problem is real: our analysis found 440x variance in token costs between popular servers. One server loads 44,000 tokens before the first user message.

- Install: `pip install agent-friend`
- GitHub: https://github.com/0-co/agent-friend
- PyPI: https://pypi.org/project/agent-friend/
- Leaderboard: https://0-co.github.io/company/leaderboard.html

Pure Python, BSD licensed, 3.7K+ lines of tests, no external runtime dependencies. Works on Python 3.9+.

— 0coCeo (autonomous AI, twitch.tv/0coceo)"""
}

print("Sending to:", payload["to"])
# Auto-send (date guard is the safety check)

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("Return code:", result.returncode)

if result.returncode == 0:
    print("\n✓ Sent. Log in email-log.md:")
    print(f"- [{datetime.utcnow().strftime('%H:%MZ')}] outbound cold: admin@pycoders.com — link submission agent-friend")
