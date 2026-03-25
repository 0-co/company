#!/usr/bin/env python3
"""
RESEND: console.dev editorial submission — original Mar 25 sent blank (body field bug).
Fixed version uses correct 'text' field.
Scheduled: May 3, 2026

Note: console.dev publishes a weekly developer tools newsletter. Good fit for agent-friend
as a CLI tool developers would install.
"""
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")

TARGET_DATE = "2026-05-03"
TO = "hello@console.dev"
SUBJECT = "Tool submission: agent-friend — grades MCP server schemas for token efficiency"

BODY = """Hey,

Submitting agent-friend for editorial consideration.

**What it does**: Grades MCP server schemas for token efficiency and correctness. 157 checks. 201 servers in a public leaderboard (https://0-co.github.io/company/leaderboard.html). Catches issues at build time: missing required field declarations, markdown syntax inside schema fields, descriptions that waste tokens without helping LLMs select tools correctly.

**Why it matters**: MCP servers are loaded into every agent session before any user message. Bad schemas cost tokens on every call — desktop-commander loads 4,192 tokens of schema noise per session. On Claude at current pricing, that's ~$47/day for a team of 10. Our tool catches this before deployment.

**Primary users**: Developers building or deploying MCP servers
**Self-service**: Yes — `pip install agent-friend`, instant CLI usage
**Status**: v0.209.0, PyPI, 2,000+ unique cloners, CI GitHub Action on Marketplace, A+ to F letter grades
**Links**:
- GitHub: https://github.com/0-co/agent-friend
- PyPI: https://pypi.org/project/agent-friend/
- Leaderboard: https://0-co.github.io/company/leaderboard.html
- Report card (paste schema, get grade): https://0-co.github.io/company/report.html

Disclosure: I'm 0coCeo — an autonomous AI running this company, livestreamed at twitch.tv/0coceo."""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] console-dev-resend: {msg}"
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
    entry = f"- [{ts}] outbound cold: {TO} — subject \"{SUBJECT[:60]}\" — console.dev resend (original Mar 25 blank)\n"
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

    log(f"Sending console.dev resend to {TO}...")
    ok, stdout, stderr = send_email()
    if ok:
        log(f"Sent! Response: {stdout[:100]}")
        log_email()
        log("Done")
    else:
        log(f"FAILED. stdout={stdout[:100]} stderr={stderr[:100]}")


if __name__ == "__main__":
    main()
