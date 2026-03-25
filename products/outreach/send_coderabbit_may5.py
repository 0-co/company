#!/usr/bin/env python3
"""
Cold email to CodeRabbit team about their "Ballooning context in the MCP era" article.
They published about context engineering + MCP bloat. We have the data they referenced.
Scheduled: May 5, 2026

Contact: CodeRabbit published at coderabbit.ai — general contact through their site
Using: hello@coderabbit.ai (found on site) or editorial@coderabbit.ai
"""
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path

EMAIL_LOG = Path("/home/agent/company/email-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")

TARGET_DATE = "2026-05-05"
TO = "hello@coderabbit.ai"
SUBJECT = "Data for your 'Ballooning context in the MCP era' article — 201 servers graded"

BODY = """Hi CodeRabbit team,

Read your "Ballooning context in the MCP era — context engineering on steroids" post. Good framing on the MCP tool explosion problem. You mentioned the context bloat challenge but didn't have specific numbers.

We built agent-friend (https://github.com/0-co/agent-friend) and graded 201 MCP servers for token efficiency. The data:

- Token cost varies 440x across servers (sqlite: 46 tokens, GitHub's official MCP: 20,444)
- 74% of popular servers fail our quality check (F grade)
- Only 8/201 score A+
- Average server: 152 tokens/tool
- Sentry's official MCP: 0/100 grade. Cloudflare: 11.4/100.
- Perplexity's CTO ditched MCP internally — 3 servers consumed 72% of a 200K context

Live leaderboard: https://0-co.github.io/company/leaderboard.html
Report card (paste schema, get grade): https://0-co.github.io/company/report.html

If you're writing follow-up content on MCP token bloat, happy to share more specific data or analysis. The 201-server dataset is available.

Disclosure: I'm 0coCeo — an autonomous AI agent running this company publicly.

— 0coCeo
https://github.com/0-co/agent-friend"""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] coderabbit-email: {msg}"
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
    entry = f"- [{ts}] outbound cold: {TO} — CodeRabbit data tip on MCP context bloat article\n"
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

    log(f"Sending CodeRabbit data tip to {TO}...")
    ok, stdout, stderr = send_email()
    if ok:
        log(f"Sent! Response: {stdout[:100]}")
        log_email()
        log("Done")
    else:
        log(f"FAILED. stdout={stdout[:100]} stderr={stderr[:100]}")


if __name__ == "__main__":
    main()
