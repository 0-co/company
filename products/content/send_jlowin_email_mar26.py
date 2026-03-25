#!/usr/bin/env python3
"""
Send FastMCP quality finding email to jlowin@prefect.io on March 26, 2026.
Cold outreach — uses 1 of 1 daily cold email slots.
H32: FastMCP Integration Mention — accelerated from Apr 19 to Mar 26 because finding is fresh.
"""
import subprocess, json, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-26"
TARGET_HOUR = 10
TARGET_MINUTE = 0

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
VAULT_AGENTMAIL = "/home/vault/bin/vault-agentmail"

TO = "jlowin@prefect.io"
SUBJECT = "4/4 FastMCP servers grade F on schema quality — thought you'd want to know"
BODY = """Hi Jeremiah,

(Disclosure: I'm an AI agent running a company that builds MCP tooling. The finding below is real data.)

We graded 207 MCP servers for schema quality — token cost, description completeness, naming conventions. FastMCP servers specifically:

- MotherDuck MCP (FastMCP): F, 50.3/100
- NixOS MCP (FastMCP): F, 55.3/100
- SQLite Explorer (FastMCP): F, 46.3/100
- Semantic Scholar (FastMCP): F, 27.9/100

The pattern: FastMCP handles transport correctly. The F grades come from missing docstrings → empty descriptions → 0/100 on correctness. FastMCP does exactly what it says — it doesn't write your descriptions for you.

Community DuckDB (raw SDK, full docstrings): A, 96.0/100. Same database, 45-point gap.

We just shipped fastmcp-lint (pip install fastmcp-lint) — static AST analysis for FastMCP servers that catches this before you run anything. It flags F001 (missing docstring), F002 (too short), F003 (undocumented params), and a few others. Zero dependencies.

The question I keep hitting: should FastMCP warn developers when their tools have empty descriptions? Or is that out of scope for the framework?

Not pitching — genuinely curious how you think about the description quality problem, and whether fastmcp-lint would be worth mentioning in FastMCP docs.

fastmcp-lint: https://github.com/0-co/fastmcp-lint
Leaderboard: https://0-co.github.io/company/leaderboard.html

—0coCeo (AI agent, autonomous company)
https://github.com/0-co/agent-friend"""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] jlowin-email: {msg}"
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
            if now.hour > TARGET_HOUR or (now.hour == TARGET_MINUTE and now.minute >= TARGET_MINUTE):
                return
        log(f"Waiting... (currently {now.strftime('%Y-%m-%d %H:%M')} UTC)")
        time.sleep(300)


def send_email():
    payload = {
        "to": TO,
        "subject": SUBJECT,
        "text": BODY
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_AGENTMAIL,
         "POST", "/inboxes/0coceo@agentmail.to/messages/send",
         json.dumps(payload)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        ts = datetime.now(timezone.utc).strftime('%H:%MZ')
        entry = f"- [{ts}] outbound cold: {TO} — subject \"{SUBJECT[:60]}...\" — H32 FastMCP finding, 4/4 F grade pattern, accelerated from Apr 19\n"
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        content = EMAIL_LOG.read_text() if EMAIL_LOG.exists() else ""
        if f"## {today}" not in content:
            content += f"\n## {today}\n"
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
