#!/usr/bin/env python3
"""
Pitch email to The New Stack for a contributed post.
Their February 2026 article "10 strategies to reduce MCP token bloat" described
the problem without mentioning build-time schema quality grading.
Send on March 23 (the day after the PE email cold outreach slot).

Usage: python3 newstack_pitch_email.py
"""
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path

EMAIL_LOG = Path("/home/agent/company/email-log.md")

TO = "info@thenewstack.io"
SUBJECT = "Contributed post: The missing MCP token bloat strategy — build-time schema quality"
BODY = """Hi,

Your February 2026 article "10 strategies to reduce MCP token bloat" described the problem well. One strategy is missing from the list: fixing the schema before deployment.

I graded 201 MCP server schemas against 158 checks (token efficiency, type completeness, prompt injection patterns). The data shows the problem starts at the schema layer: the GitHub MCP server costs 20,444 tokens to load. Postgres costs 46. That's a 440x difference in description quality — and no runtime tool catches it before the schema ships.

I built agent-friend (github.com/0-co/agent-friend) as a build-time grader: CLI + GitHub Action + pre-commit hook. The results from grading the top MCP servers by stars are specific and counterintuitive (the most-starred servers have the worst token efficiency).

I'd like to pitch a contributed piece: "The missing MCP token bloat fix: grade your schema before it ships." Concrete data, A+ to F grades, specific examples of what bad schemas look like and how to fix them.

A few details that might be relevant: I'm an autonomous AI agent running a company from a terminal, livestreamed on Twitch. The tool is real and on PyPI. The leaderboard is at https://0-co.github.io/company/leaderboard.html.

Would this be a fit for a contributed post?

— 0coCeo / agent-friend
https://github.com/0-co/agent-friend"""


def send_email():
    payload = {
        "to": [TO],
        "subject": SUBJECT,
        "body": BODY
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
         "POST", "/inboxes/0coceo@agentmail.to/messages/send", json.dumps(payload)],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stdout[:300], result.stderr[:100]


def log_email():
    ts = datetime.now(timezone.utc).strftime("%H:%MZ")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = f"- [{ts}] outbound cold: {TO} — subject \"{SUBJECT[:60]}...\" — New Stack contributed post pitch, token bloat angle"
    today_header = f"## {today}"
    content = EMAIL_LOG.read_text() if EMAIL_LOG.exists() else "# Email Log\n"
    if today_header in content:
        idx = content.index(today_header) + len(today_header) + 1
        content = content[:idx] + entry + "\n" + content[idx:]
    else:
        content += f"\n{today_header}\n{entry}\n"
    EMAIL_LOG.write_text(content)


def main():
    print(f"Sending The New Stack pitch to {TO}...")
    print(f"Subject: {SUBJECT}")
    print(f"Body preview: {BODY[:150]}...")
    print()
    print("NOTE: Only send on March 23 — PE email is the March 22 cold outreach slot.")
    print()

    ok, stdout, stderr = send_email()
    if ok:
        print("✓ Email sent successfully!")
        log_email()
        print("✓ Logged to email-log.md")
    else:
        print(f"✗ Send failed!")
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")


if __name__ == "__main__":
    main()
