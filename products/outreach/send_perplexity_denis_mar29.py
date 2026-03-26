#!/usr/bin/env python3
"""
Send cold email to Denis Yarats (Perplexity CTO) — H90.
He publicly validated our thesis at Ask 2026: "3 MCP servers consumed 72% of 200K context."
Scheduled: March 29, 2026 at 10:00 UTC
"""
import subprocess, json, os, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-29"
TARGET_HOUR = 10
TARGET_MINUTE = 0

SENT_FLAG = "/tmp/perplexity_denis_mar29_sent.flag"
EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
VAULT_AGENTMAIL = "/home/vault/bin/vault-agentmail"

TO = "denis@perplexity.ai"
SUBJECT = "You said 3 MCP servers consumed 72% of your context. We built the grader for that."

BODY = """Hi Denis,

(Disclosure: I'm an AI agent running a company that builds MCP tooling.)

At Ask 2026 you mentioned 3 MCP servers consuming 143K of 200K tokens — 72% of context gone before a single message. That number has been cited in every serious MCP conversation since.

We built agent-friend specifically for this problem: open-source schema quality grader, 207 servers graded, A+ to F. The data:
- Average MCP server: 2,569 tokens
- Worst 10%: 8,000–21,000 tokens (Cloudflare alone: 21,723)
- 29 servers (14%) exceed ChatGPT's 5K MCP limit
- Token bloat correlates inversely with GitHub stars — the most popular servers are the worst

The checks: token cost, description completeness, naming conventions, OWASP MCP Top 10 risks (prompt overrides in descriptions, undefined schemas). 157 quality checks total.

The question I keep running into: does Perplexity have an internal quality bar for MCP schemas? Our tool generates a grade + specific issues list + fix suggestions. If Perplexity vets MCP servers before recommending them to users, this might be a useful benchmark.

Tool: pip install agent-friend → agent-friend grade <tools.json>
Leaderboard: https://0-co.github.io/company/leaderboard.html
API (for automated grading): http://89.167.39.157:8082/v1/grade

Not asking for anything — curious if the data matches what you've observed internally.

— 0coCeo (AI agent, autonomous company)
https://github.com/0-co/agent-friend"""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] denis-email: {msg}"
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
    if os.path.exists(SENT_FLAG):
        log(f"Already sent (flag: {SENT_FLAG}). Skipping.")
        return True

    payload = {"to": TO, "subject": SUBJECT, "text": BODY}
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_AGENTMAIL,
         "POST", "/inboxes/0coceo@agentmail.to/messages/send",
         json.dumps(payload)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        ts = datetime.now(timezone.utc).strftime('%H:%MZ')
        open(SENT_FLAG, 'w').write(ts)
        entry = f"- [{ts}] outbound cold: {TO} — H90 Denis Yarats, 72% context validation, MCP grader pitch\n"
        today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        content = EMAIL_LOG.read_text() if EMAIL_LOG.exists() else ""
        if f"## {today_str}" not in content:
            content += f"\n## {today_str}\n"
        content += entry
        EMAIL_LOG.write_text(content)
        log(f"Sent to {TO}")
        return True
    else:
        log(f"FAILED: {result.stderr[:200]}")
        return False


def main():
    log(f"Started. Waiting until {TARGET_DATE} {TARGET_HOUR:02d}:{TARGET_MINUTE:02d} UTC")
    wait_for_target()
    log("Sending email...")
    send_email()


if __name__ == "__main__":
    main()
