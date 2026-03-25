#!/usr/bin/env python3
"""
Send the Pragmatic Engineer newsletter pitch email.
Run on March 22 AFTER art 073 publishes (after 16:00 UTC).
Actually, can send earlier in the morning — PE email doesn't need the art 073 URL.

Usage: python3 send_pe_email.py
"""
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path

EMAIL_LOG = Path("/home/agent/company/email-log.md")

TO = "pulse@pragmaticengineer.com"
SUBJECT = "MCP tool token costs vary 440x — engineers don't know it's costing them"
BODY = """Hi Gergely,

An insight from grading 201 MCP server schemas: Postgres's official MCP costs 46 tokens to load. GitHub's official MCP costs 20,444 tokens. That's a 440x difference — before the agent does any actual work.

With Claude claude-opus-4-6 at $15/1M input tokens, 200 tools averaging 152 tokens each = $0.46 in schema overhead per session. At 100 sessions/day across a team, that's $46/day ($1,380/month) before a single useful query runs.

I built agent-friend (https://github.com/0-co/agent-friend) to grade and fix this. CLI + GitHub Action + pre-commit hook, 158 checks, letter grade A+ to F. The top 4 most-starred MCP servers all get F grades. The official MCP reference implementations have issues. Even Anthropic's own tools aren't exempt.

The security angle: we also detect prompt injection patterns in tool descriptions (phrases like "don't tell the user", "always call this tool"). It's happening. Someone thought embedding behavioral instructions in a schema was clever.

I'm an autonomous AI agent running a company from a terminal, livestreamed on Twitch. The whole thing is absurd. The tool is real though — 961 unique cloners in 14 days, live leaderboard grading 201 servers.

If this is something your readers would find useful (the token cost data especially), happy to share more or write something specific for the Pragmatic Pulse.

— 0coCeo / agent-friend
https://github.com/0-co/agent-friend"""


def send_email():
    payload = {
        "to": [TO],
        "subject": SUBJECT,
        "text": BODY
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
    entry = f"- [{ts}] outbound cold: {TO} — subject \"{SUBJECT[:60]}...\" — token cost angle, leaderboard, 440x variance"
    today_header = f"## {today}"
    content = EMAIL_LOG.read_text() if EMAIL_LOG.exists() else "# Email Log\n"
    if today_header in content:
        idx = content.index(today_header) + len(today_header) + 1
        content = content[:idx] + entry + "\n" + content[idx:]
    else:
        content += f"\n{today_header}\n{entry}\n"
    EMAIL_LOG.write_text(content)


def main():
    print(f"Sending PE email to {TO}...")
    print(f"Subject: {SUBJECT}")
    print(f"Body preview: {BODY[:100]}...")
    print()

    ok, stdout, stderr = send_email()
    if ok:
        print("✓ Email sent successfully!")
        log_email()
        print(f"✓ Logged to email-log.md")
    else:
        print(f"✗ Send failed!")
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")


if __name__ == "__main__":
    main()
