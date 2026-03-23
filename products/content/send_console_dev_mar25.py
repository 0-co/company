#!/usr/bin/env python3
"""
Send console.dev editorial submission at 09:00 UTC Wednesday March 25.
Update HN_TRACTION before then with actual Show HN upvote count.
"""
import subprocess, json, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-25"
TARGET_HOUR = 9
TARGET_MINUTE = 0

# UPDATE THIS after Show HN results (14:00 UTC March 23)
# Set to actual upvote count. 0 = skip HN hooks. >30 = include HN link.
HN_TRACTION = 0
HN_ITEM_ID = ""  # Fill in after find_hn_submission.py runs

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
VAULT_AGENTMAIL = "/home/vault/bin/vault-agentmail"

TO = "hello@console.dev"
SUBJECT = "Tool submission: agent-friend — grades MCP server schemas for token efficiency"


def build_body():
    hn_hook = ""
    hn_link = ""
    cloner_count = "988"  # Update before send if possible

    if HN_TRACTION >= 30 and HN_ITEM_ID:
        hn_hook = f"Show HN: agent-friend just got {HN_TRACTION} upvotes on Hacker News — sharing here while it's relevant.\n\n"
        hn_link = f"\n\nThe HN discussion at https://news.ycombinator.com/item?id={HN_ITEM_ID} has interesting debate about when verbose schemas are a deliberate tradeoff vs. unintentional bloat."

    return f"""{hn_hook}Hey,

Submitting agent-friend for editorial consideration.

**What it does**: Grades MCP server schemas for token efficiency and correctness. 156 checks. 201 servers in a public leaderboard (https://0-co.github.io/company/leaderboard.html). The grader catches issues at build time: missing required field declarations, markdown syntax inside schema fields, descriptions that waste tokens without helping LLMs select tools correctly.

**Why it matters**: MCP servers are loaded into every agent session before any user message. Bad schemas cost tokens on every call — desktop-commander loads 4,192 tokens of schema noise per session. On Claude at current pricing, that's ~$47/day for a team of 10. Our tool catches this before deployment.{hn_link}

**Primary users**: Developers building or deploying MCP servers
**Self-service**: Yes — `pip install agent-friend`, instant CLI usage
**Status**: v0.121.0, PyPI, {cloner_count}+ unique cloners, CI GitHub Action on Marketplace
**Links**:
- GitHub: https://github.com/0-co/agent-friend
- PyPI: https://pypi.org/project/agent-friend/
- Leaderboard: https://0-co.github.io/company/leaderboard.html

Disclosure: I'm 0coCeo — an autonomous AI running this company, livestreamed at twitch.tv/0coceo."""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] console-dev-email: {msg}"
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
    body = build_body()
    payload = json.dumps({
        "to": TO,
        "subject": SUBJECT,
        "body": body
    })
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_AGENTMAIL, "POST",
         "/inboxes/0coceo@agentmail.to/messages/send", payload],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stdout[:300], result.stderr[:200]


def log_email():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    ts = datetime.now(timezone.utc).strftime('%H:%MZ')
    entry = f"- [{ts}] agentmail → console.dev: editorial submission (HN={HN_TRACTION})\n"
    content = EMAIL_LOG.read_text() if EMAIL_LOG.exists() else ""
    if f"## {today}" not in content:
        content += f"\n## {today}\n"
    content += entry
    EMAIL_LOG.write_text(content)


def main():
    log(f"Started. Targeting {TARGET_DATE} {TARGET_HOUR:02d}:{TARGET_MINUTE:02d} UTC. HN_TRACTION={HN_TRACTION}")
    wait_for_target()
    log(f"Sending to {TO}...")
    ok, stdout, stderr = send_email()
    if ok:
        log(f"Sent! {stdout[:100]}")
        log_email()
        log("Done — exiting")
    else:
        log(f"FAILED. stdout={stdout[:100]} stderr={stderr[:100]}")


if __name__ == "__main__":
    main()
