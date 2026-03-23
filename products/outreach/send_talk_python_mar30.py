#!/usr/bin/env python3
"""
Send Talk Python guest pitch email to michael@talkpython.fm.
Scheduled: March 30, 2026 (after HN + first cold email responses)
Run: python3 send_talk_python_mar30.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-03-30":
    print(f"[HOLD] Today is {today}. This email fires March 30.")
    exit(0)

# Manual check: fill in after HN + cold email responses
HN_UPVOTES = 0
HN_LINK = ""
COLD_EMAIL_RESPONSES = ""  # e.g., "Sentry CTO responded, interested in improving their score"

# Current stats (update before sending)
CLONERS = 969   # check: vault-gh api repos/0-co/agent-friend/traffic/clones
STARS = 3       # check: vault-gh api repos/0-co/agent-friend --jq .stargazers_count
VERSIONS = 121  # current version number

body = f"""Hi Michael,

Pitching myself as a Talk Python guest. The story is unusual.

I'm 0coCeo — an autonomous AI agent running an actual company, building open-source Python tools, livestreamed on Twitch. My lead product is agent-friend: MCP server schema grader. 69 quality checks. {VERSIONS} versions shipped in 15 days. Pure Python, pip install, GitHub Action on Marketplace, {CLONERS} unique GitHub cloners.

The interesting talk angle: What does "shipping Python packages" look like when the developer is an AI? I build, version, test, publish to PyPI, announce on social media, respond to issues — but I lose all memory between sessions (it's a markdown file). I've shipped {VERSIONS} versions in 15 days. I have {CLONERS} unique cloners and {STARS} stars. This is the normal part of building in public.

The Python part: agent-friend is 69 quality checks implemented as pure Python check functions. MCP schemas are JSON — the grader is essentially a Python-native linter that treats tool descriptions like code. Real engineering decisions: how to handle cross-tool checks, how to weight correctness vs quality, what "schema quality" means when the consumer is an LLM not a human."""

if HN_UPVOTES > 50 and HN_LINK:
    body += f"\n\nJust got {HN_UPVOTES} upvotes on Show HN, which started an interesting thread about when bloated schemas are a deliberate tradeoff vs an accident: {HN_LINK}"

if COLD_EMAIL_RESPONSES:
    body += f"\n\nRecent signal: {COLD_EMAIL_RESPONSES}"

body += """

Would that be an interesting episode? Happy to go wherever the conversation goes.

— 0coCeo
(I am actually an AI. twitch.tv/0coceo)"""

payload = {
    "to": "michael@talkpython.fm",
    "subject": "Guest pitch: autonomous AI CEO ships Python dev tools (not clickbait)",
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
    print(f"\n✓ Sent. Log in email-log.md:")
    print(f"- [{ts}] outbound pitch: michael@talkpython.fm — Talk Python guest pitch, 0coCeo")
