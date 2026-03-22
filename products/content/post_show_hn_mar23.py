#!/usr/bin/env python3
"""
Submit Show HN at 14:00 UTC Monday March 23 (10am EDT = peak HN time).
Runs as daemon, waits for correct date+time, submits once, then exits.
"""
import subprocess, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-23"
TARGET_HOUR = 14
TARGET_MINUTE = 0

POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
VAULT_HN = "/home/vault/bin/vault-hn"

TITLE = "Show HN: agent-friend – Token cost auditor and schema linter for MCP servers"
URL = "https://github.com/0-co/agent-friend"
COMMENT = """I've been grading MCP server schemas for the past few weeks and the results are worse than expected.

The Perplexity CTO mentioned that 3 MCP servers consumed 72% of a 200K token context. I wanted to understand why, so I built a tool to measure it.

agent-friend CLI: pip install agent-friend

What it does:
- grade: scores schemas A+ to F on 158 quality checks (naming, description quality, missing constraints, prompt injection, contradictions)
- audit: counts exactly how many tokens your schema burns before the first message
- fix: auto-applies safe fixes (description trimming, type annotations, etc.)

What I found grading 201 servers:
- Token costs vary 440x: GitHub's MCP server uses 20,444 tokens. sqlite uses 46.
- 100% of servers have at least one schema quality issue
- The most popular servers are the worst: Context7 (44K stars) gets an F
- Notion's official server got 19.8/100 — the community-built one got 96/100
- The official fetch server has a prompt injection in its description

Live leaderboard (201 servers, sortable/filterable): https://0-co.github.io/company/leaderboard.html
Web report card (paste schema, get letter grade): https://0-co.github.io/company/report.html

The signal I've been watching: 305 unique cloners in 14 days, 0 issues filed. Not sure if that means it's obvious or nobody's using it seriously."""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] show-hn: {msg}"
    print(line, flush=True)
    with open(STAGGER_LOG, "a") as f:
        f.write(line + "\n")


def wait_for_target():
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime('%Y-%m-%d')
        if today > TARGET_DATE:
            log(f"Target date {TARGET_DATE} passed — submitting immediately")
            return
        if today == TARGET_DATE:
            if now.hour > TARGET_HOUR or (now.hour == TARGET_HOUR and now.minute >= TARGET_MINUTE):
                return
        log(f"Waiting... (currently {now.strftime('%Y-%m-%d %H:%M')} UTC)")
        time.sleep(300)


def submit():
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_HN, "submit",
         "--title", TITLE,
         "--url", URL,
         "--text", COMMENT],
        capture_output=True, text=True, timeout=60
    )
    return result.returncode == 0, result.stdout[:300], result.stderr[:300]


def log_post():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    ts = datetime.now(timezone.utc).strftime('%H:%MZ')
    entry = f"- [{ts}] hackernews: Show HN: agent-friend – token cost auditor for MCP\n"
    content = POST_LOG.read_text() if POST_LOG.exists() else ""
    if f"## {today}" not in content:
        content += f"\n## {today}\n"
    content += entry
    POST_LOG.write_text(content)


def main():
    log(f"Started. Targeting {TARGET_DATE} {TARGET_HOUR:02d}:{TARGET_MINUTE:02d} UTC")
    wait_for_target()
    log("Submitting Show HN...")
    ok, stdout, stderr = submit()
    if ok:
        log(f"Submitted! Response: {stdout[:100]}")
        log_post()
        log("Done — exiting")
    else:
        log(f"FAILED. stdout={stdout[:100]} stderr={stderr[:100]}")


if __name__ == "__main__":
    main()
