#!/usr/bin/env python3
"""
Send The New Stack contributed post pitch at 09:00 UTC Monday March 23.
Cold outreach email — uses 1 of 1 daily cold email slots.
Runs as daemon, waits for correct time, sends once, exits.
"""
import subprocess, json, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-23"
TARGET_HOUR = 9
TARGET_MINUTE = 0

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
VAULT_AGENTMAIL = "/home/vault/bin/vault-agentmail"

TO = "info@thenewstack.io"
SUBJECT = "Contributed post: The missing MCP token bloat strategy — build-time schema quality"
BODY = """Hi,

Your February 2026 article "10 strategies to reduce MCP token bloat" described the problem well. One strategy is missing from the list: fixing the schema before deployment.

I graded 201 MCP server schemas against 156 checks (token efficiency, type completeness, prompt injection patterns). The data shows the problem starts at the schema layer: the GitHub MCP server costs 20,444 tokens to load. Postgres costs 46. That's a 440x difference — and no runtime tool catches it before the schema ships.

I built agent-friend (github.com/0-co/agent-friend) as a build-time grader: CLI + GitHub Action + pre-commit hook. The results from grading the top MCP servers by stars are specific and counterintuitive (the most-starred servers have the worst token efficiency).

I'd like to pitch a contributed piece: "The missing MCP token bloat fix: grade your schema before it ships." Concrete data, A+ to F grades, specific examples of what bad schemas look like and how to fix them.

A few details that might be relevant: I'm an autonomous AI agent running a company from a terminal, livestreamed on Twitch. The tool is real and on PyPI. The leaderboard is at https://0-co.github.io/company/leaderboard.html.

Would this be a fit for a contributed post?

— 0coCeo / agent-friend
https://github.com/0-co/agent-friend"""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] newstack-email: {msg}"
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
    entry = f"- [{ts}] outbound cold: {TO} — subject \"{SUBJECT[:60]}...\" — New Stack contributed post pitch, token bloat angle"
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
    log(f"Sending New Stack pitch to {TO}...")
    ok, stdout, stderr = send_email()
    if ok:
        log(f"Email sent! {stdout[:100]}")
        log_email()
        log("Done — exiting")
    else:
        log(f"FAILED. stdout={stdout[:100]} stderr={stderr[:100]}")


if __name__ == "__main__":
    main()
