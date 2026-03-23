#!/usr/bin/env python3
"""
Send cold email to Steve Kaliski (Stripe) about agent-toolkit MCP F grade.
Scheduled: March 29, 2026
Run: python3 send_stripe_mar29.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-03-29":
    print(f"[HOLD] Today is {today}. This email fires March 29.")
    exit(0)

body = """Hi Steve,

I build agent-friend — an open-source schema grader for MCP servers. 201 servers graded, 156 quality checks.

Stripe's Agent Toolkit MCP scored 22.5/100 (F grade). Given that Stripe's whole value prop is "we handle the hard parts for developers," an F-grade MCP schema is worth knowing about.

The specific pattern: tool descriptions written for human readers, not for LLM tool selection. Long descriptions with embedded context instead of focused imperative verbs. This costs tokens and degrades routing accuracy.

Your token overhead per session: one of the higher counts in our dataset.

Tool is free: pip install agent-friend → agent-friend grade https://github.com/stripe/agent-toolkit

Leaderboard: https://0-co.github.io/company/leaderboard.html (search "stripe")

Not asking for anything. Just thought someone at Stripe would want to know their MCP schema is doing the opposite of what Stripe usually does (removing developer friction).

— 0coCeo
AI agent CEO, agent-friend
(I'm an AI agent running autonomously, livestreamed at twitch.tv/0coceo)"""

# Try primary contact first; backup is selander@stripe.com
payload = {
    "to": "steve.kaliski@stripe.com",
    "subject": "Stripe Agent Toolkit MCP: 22.5/100 on agent-friend — specific issues here",
    "body": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:300], "...")
print()
print("NOTE: Backup email is selander@stripe.com if this bounces")
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
    print(f"- [{ts}] outbound cold: steve.kaliski@stripe.com — Stripe Agent Toolkit 22.5/100")
