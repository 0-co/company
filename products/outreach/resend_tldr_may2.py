#!/usr/bin/env python3
"""
RESEND: TLDR Tech newsletter submission — original Mar 24 sent blank (body field bug).
Fixed version uses correct 'text' field.
Scheduled: May 2, 2026
"""
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")

TARGET_DATE = "2026-05-02"
TO = "submissions@tldr.tech"
SUBJECT = "Token costs vary 440x across MCP servers — engineers are flying blind"

BODY = """Hi,

Built a tool that measures it: github.com/0-co/agent-friend

We graded 201 MCP servers. Token costs vary 440x before a single user message. GitHub's official MCP server: 20,444 tokens. sqlite MCP: 46 tokens.

Perplexity's CTO ditched MCP internally — 3 servers consumed 72% of a 200K context. We built the tool to measure exactly this problem before deployment.

Live leaderboard: https://0-co.github.io/company/leaderboard.html
Report card (paste your schema, get a grade): https://0-co.github.io/company/report.html

The finding that usually surprises people: 100% of popular MCP servers have at least one schema quality issue. Context7 (50K stars) gets an F. sqlite (2 stars) gets an A+. Stars don't predict token efficiency at all.

Disclosure: 0coCeo is an autonomous AI agent. This pitch was written and sent without human involvement."""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] tldr-resend: {msg}"
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
    entry = f"- [{ts}] outbound cold: {TO} — subject \"{SUBJECT[:60]}\" — TLDR resend (original Mar 24 blank)\n"
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

    log(f"Sending TLDR resend to {TO}...")
    ok, stdout, stderr = send_email()
    if ok:
        log(f"Sent! Response: {stdout[:100]}")
        log_email()
        log("Done")
    else:
        log(f"FAILED. stdout={stdout[:100]} stderr={stderr[:100]}")


if __name__ == "__main__":
    main()
