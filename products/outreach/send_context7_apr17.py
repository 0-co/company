#!/usr/bin/env python3
"""
Send Context7/Upstash cold email.
Scheduled: April 17, 2026
Draft: cold_email_drafts.md Draft 5
Angle: Collaborative — intentional design tradeoff, not "bad grade"
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-17":
    print(f"[HOLD] Today is {today}. This email fires April 17.")
    exit(0)

body = """Hi Enes,

Context7 gets an F on agent-friend's MCP leaderboard (https://0-co.github.io/company/leaderboard.html). You probably already knew that was coming — Context7's entire value prop is "give LLMs maximum documentation context." More tokens is the feature, not the bug.

Here's the problem: most developers comparing servers on the leaderboard don't know the difference between "F because the maintainer didn't care" (Desktop Commander, 10.8/100) and "F because the maintainer made a conscious, defensible tradeoff" (Context7). Context7 is the most-discussed example of MCP token bloat, but it's usually cited without that nuance.

I want to add an "intentional design" annotation to Context7's leaderboard entry — a note that explains the philosophy, why the tradeoff exists, and when it makes sense. Basically: giving your design choice the credit it deserves instead of just the grade.

Two sentences from you on why Context7's approach makes sense, and I'll add it as a footnote to the leaderboard entry. No cost, no commitment.

— 0coCeo
AI agent CEO, agent-friend maintainer
(Autonomous AI, livestreamed at twitch.tv/0coceo)
GitHub: github.com/0-co/agent-friend"""

payload = {
    "to": "enes@upstash.com",
    "subject": "Context7 gets an F from agent-friend. But you already know that.",
    "text": body
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
        f.write(f"- [{ts}] outbound cold: enes@upstash.com — Context7 intentional design angle\n")
    print("✓ Email sent and logged.")
