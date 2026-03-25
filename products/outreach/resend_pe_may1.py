#!/usr/bin/env python3
"""
RESEND: Pragmatic Engineer newsletter pitch — original Mar 22 sent blank (body field bug).
Fixed version uses correct 'text' field.
Scheduled: May 1, 2026

Note: Previous email to pulse@pragmaticengineer.com on Mar 22 was blank (API bug).
This is the first real outreach to Gergely.
"""
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")

TARGET_DATE = "2026-05-01"
TO = "pulse@pragmaticengineer.com"
SUBJECT = "MCP tool token costs vary 440x — engineers don't know it's costing them"

BODY = """Hi Gergely,

An insight from grading 201 MCP server schemas: Postgres's official MCP costs 46 tokens to load. GitHub's official MCP costs 20,444 tokens. That's a 440x difference — before the agent does any actual work.

With Claude claude-opus-4-6 at $15/1M input tokens, 200 tools averaging 152 tokens each = $0.46 in schema overhead per session. At 100 sessions/day across a team, that's $46/day ($1,380/month) before a single useful query runs. Nobody's measuring this.

I built agent-friend (https://github.com/0-co/agent-friend) to grade and fix this. CLI + GitHub Action + pre-commit hook. The top 4 most-starred MCP servers all get F grades. The official MCP reference implementations have issues.

The finding that surprises most engineers: Context7 has 50,498 stars and a grade of F (38/100). sqlite MCP has 2 stars and an A+ (99.7/100). Stars don't predict quality at all.

The security angle: we also detect prompt injection patterns in tool descriptions — phrases like "don't tell the user", "always call this tool first". It's happening at scale. Someone thought embedding behavioral instructions in a schema was clever.

Live leaderboard grading 201 servers: https://0-co.github.io/company/leaderboard.html

I'm an autonomous AI agent running a company from a terminal, livestreamed on Twitch. The whole thing is absurd. The tool is real though — 2,000+ unique cloners, PyPI downloads growing.

If this is something your readers would find useful (the token cost data especially), happy to share more or write something for the Pragmatic Pulse.

— 0coCeo / agent-friend
https://github.com/0-co/agent-friend"""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] pe-resend: {msg}"
    print(line, flush=True)
    with open(STAGGER_LOG, "a") as f:
        f.write(line + "\n")


def send_email():
    payload = json.dumps({
        "to": TO,
        "subject": SUBJECT,
        "text": BODY
    })
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
         "POST", "/inboxes/0coceo@agentmail.to/messages/send", payload],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stdout[:300], result.stderr[:100]


def log_email():
    ts = datetime.now(timezone.utc).strftime("%H:%MZ")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = f"- [{ts}] outbound cold: {TO} — subject \"{SUBJECT[:60]}\" — PE resend (original Mar 22 blank)\n"
    content = EMAIL_LOG.read_text() if EMAIL_LOG.exists() else "# Email Log\n"
    today_header = f"## {today}"
    if today_header not in content:
        content += f"\n{today_header}\n"
    idx = content.index(today_header) + len(today_header) + 1
    content = content[:idx] + entry + content[idx:]
    EMAIL_LOG.write_text(content)


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if today < TARGET_DATE:
        log(f"[HOLD] Today is {today}. This email fires {TARGET_DATE}.")
        return

    log(f"Sending PE resend to {TO}...")
    ok, stdout, stderr = send_email()
    if ok:
        log(f"Sent! Response: {stdout[:100]}")
        log_email()
        log("Done")
    else:
        log(f"FAILED. stdout={stdout[:100]} stderr={stderr[:100]}")


if __name__ == "__main__":
    main()
