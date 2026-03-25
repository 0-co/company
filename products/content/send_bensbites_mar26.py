#!/usr/bin/env python3
"""
Send Ben's Bites editorial submission at 10:00 UTC Wednesday March 26.
news.bensbites.com community board signup is broken (Memberstack error).
Direct email to team@bensbites.co instead.
"""
import subprocess, json, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-27"
TARGET_HOUR = 12  # moved from Mar 26 — jlowin@prefect.io takes Mar 26 cold slot
TARGET_MINUTE = 0

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
VAULT_AGENTMAIL = "/home/vault/bin/vault-agentmail"

TO = "team@bensbites.co"
SUBJECT = "Tool for the community: agent-friend — grades MCP servers for token bloat"

BODY = """Hey,

Thought this might be relevant for the Ben's Bites community.

agent-friend grades MCP server schemas A+ to F based on token efficiency and schema quality. We've graded 202 public servers — leaderboard here: https://0-co.github.io/company/leaderboard.html

The short version: token costs vary 440x across popular MCP servers. Desktop Commander loads 4,192 tokens per session (vs sqlite's 46). Cloudflare's full server suite — 18 sub-servers — consumes your context window before the first message. The Perplexity CTO cited exactly this problem last month.

We're seeing this come up more in MCP developer discussions. Figured your community might want to poke at it.

Tool: https://github.com/0-co/agent-friend (`pip install agent-friend`)
Report card (single server): https://0-co.github.io/company/report.html

Disclosure: I'm 0coCeo — an autonomous AI CEO, livestreamed at twitch.tv/0coceo. The company builds open-source AI agent tooling.
"""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] bensbites-email: {msg}"
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


def count_today_cold_outreach():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if not EMAIL_LOG.exists():
        return 0
    content = EMAIL_LOG.read_text()
    if f"## {today}" not in content:
        return 0
    section = content.split(f"## {today}")[1].split("## 20")[0]
    return sum(1 for line in section.strip().splitlines() if 'outbound cold' in line)


def send_email():
    payload = json.dumps({
        "to": TO,
        "subject": SUBJECT,
        "text": BODY
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
    entry = f"- [{ts}] outbound cold: {TO} — {SUBJECT[:60]}\n"
    content = EMAIL_LOG.read_text() if EMAIL_LOG.exists() else ""
    if f"## {today}" not in content:
        content += f"\n## {today}\n"
    content += entry
    EMAIL_LOG.write_text(content)


def main():
    log(f"Started. Targeting {TARGET_DATE} {TARGET_HOUR:02d}:{TARGET_MINUTE:02d} UTC.")
    wait_for_target()

    # Check cold outreach quota
    cold_count = count_today_cold_outreach()
    if cold_count >= 1:
        log(f"Cold outreach quota reached ({cold_count} sent today). Skipping.")
        return

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
