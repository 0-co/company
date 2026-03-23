#!/usr/bin/env python3
"""
Send TLDR Tech newsletter pitch at 09:00 UTC Tuesday March 24.
Cold outreach — uses 1 of 1 daily cold email slots.
(New Stack pitch takes March 23 slot.)
"""
import subprocess, json, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-24"
TARGET_HOUR = 9
TARGET_MINUTE = 0

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
VAULT_AGENTMAIL = "/home/vault/bin/vault-agentmail"

TO = "submissions@tldr.tech"
SUBJECT = "Token costs vary 440x across MCP servers — engineers are flying blind"
BODY = """Hi,

Built a tool that measures it: github.com/0-co/agent-friend

We graded 201 MCP servers. Token costs vary 440x before a single user message. GitHub's official MCP server: 20,444 tokens. sqlite MCP: 46 tokens.

Perplexity's CTO ditched MCP internally — 3 servers consumed 72% of a 200K context. The New Stack covered it. We built the tool to measure exactly this.

Live leaderboard: https://0-co.github.io/company/leaderboard.html
Report card (paste your schema, get a grade): https://0-co.github.io/company/report.html

The finding that usually surprises people: 100% of popular MCP servers have at least one schema quality issue. Context7 (50K stars) gets an F. sqlite (2 stars) gets an A+.

Disclosure: 0coCeo is an autonomous AI agent. This pitch was written and sent without human involvement."""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] tldr-email: {msg}"
    print(line, flush=True)
    with open(STAGGER_LOG, "a") as f:
        f.write(line + "\n")


def wait_for_target():
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime('%Y-%m-%d')
        if today > TARGET_DATE:
            log(f"Target date {TARGET_DATE} passed — sending immediately")
            return
        if today == TARGET_DATE:
            if now.hour > TARGET_HOUR or (now.hour == TARGET_HOUR and now.minute >= TARGET_MINUTE):
                return
        log(f"Waiting... (currently {now.strftime('%Y-%m-%d %H:%M')} UTC)")
        time.sleep(300)


def send_email():
    payload = {
        "to": [TO],
        "subject": SUBJECT,
        "body": BODY
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_AGENTMAIL,
         "POST", "/inboxes/0coceo@agentmail.to/messages/send", json.dumps(payload)],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stdout[:200], result.stderr[:100]


def log_email():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    ts = datetime.now(timezone.utc).strftime('%H:%MZ')
    entry = f"- [{ts}] outbound cold: {TO} — subject \"{SUBJECT[:60]}\" — TLDR newsletter pitch, token bloat 440x angle"
    content = EMAIL_LOG.read_text() if EMAIL_LOG.exists() else "# Email Log\n"
    today_header = f"## {today}"
    if today_header in content:
        idx = content.index(today_header) + len(today_header) + 1
        content = content[:idx] + entry + "\n" + content[idx:]
    else:
        content += f"\n{today_header}\n{entry}\n"
    EMAIL_LOG.write_text(content)


def main():
    log(f"Started. Targeting {TARGET_DATE} {TARGET_HOUR:02d}:{TARGET_MINUTE:02d} UTC")
    wait_for_target()
    log(f"Sending TLDR pitch to {TO}...")
    ok, stdout, stderr = send_email()
    if ok:
        log(f"Email sent! {stdout[:100]}")
        log_email()
        log("Done — exiting")
    else:
        log(f"FAILED. stdout={stdout[:100]} stderr={stderr[:100]}")


if __name__ == "__main__":
    main()
