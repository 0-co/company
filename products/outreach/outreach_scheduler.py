#!/usr/bin/env python3
"""
Outreach scheduler — runs send_*.py scripts on their scheduled dates.
Runs as a daemon, checks daily, fires each script once on its target date.

Run: nohup python3 outreach_scheduler.py > /tmp/outreach_scheduler.log 2>&1 &
"""
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path("/home/agent/company/products/outreach")
LOG_FILE = Path("/tmp/outreach_scheduler.log")
EMAIL_LOG = Path("/home/agent/company/email-log.md")
FIRED_LOG = Path("/home/agent/company/products/outreach/fired.log")

# Each: (date_string, script_filename)
SCHEDULE = [
    # Max 1 cold outreach per day
    ("2026-03-25", "send_console_dev_mar25.py"),
    ("2026-03-26", "send_sentry_mar26.py"),
    ("2026-03-27", "send_cloudflare_mar27.py"),
    ("2026-03-28", "send_neon_mar28.py"),
    ("2026-03-29", "send_stripe_mar29.py"),
    ("2026-03-30", "send_pycoders_weekly_mar30.py"),
    ("2026-03-31", "send_python_bytes_mar25.py"),   # moved from Mar 25 (1/day limit)
    ("2026-04-01", "send_talk_python_mar30.py"),    # moved from Mar 30/31 (1/day limit)
    ("2026-04-02", "send_latent_space_apr1.py"),    # moved from Apr 1
    ("2026-04-03", "send_devops_weekly_apr2.py"),   # moved from Apr 2
    ("2026-04-04", "send_changelog_apr3.py"),       # moved from Apr 3
    ("2026-04-05", "send_mcpjam_apr1.py"),       # MCPJam newsletter — "Postman for MCP", 1.8K stars
    ("2026-04-26", "send_import_python_apr4.py"),  # moved from Apr 4/5 (conflicts), appended to end
    ("2026-04-06", "send_linear_apr6.py"),
    ("2026-04-07", "send_posthog_apr7.py"),
    ("2026-04-08", "send_python_weekly_apr8.py"),
    ("2026-04-09", "send_sed_apr9.py"),
    ("2026-04-10", "send_stacklok_apr10.py"),  # Stacklok ToolHive — runtime complement, hello@stacklok.com
    ("2026-04-11", "send_plane_apr11.py"),
    ("2026-04-12", "send_pulsemcp_registry_apr12.py"),
    ("2026-04-13", "send_mcpservers_registry_apr13.py"),
    ("2026-04-14", "send_glama_registry_apr14.py"),
    ("2026-04-15", "send_swirlai_newsletter_apr15.py"),
    ("2026-04-16", "send_mcp2cli_stephan_apr16.py"),
    ("2026-04-17", "send_context7_apr17.py"),
    ("2026-04-18", "send_desktop_commander_apr18.py"),
    ("2026-04-19", "send_fastmcp_jlowin_apr19.py"),
    ("2026-04-20", "send_queens_researchers_apr20.py"),
    ("2026-04-21", "send_ucla_mcp_apr21.py"),
    ("2026-04-22", "send_thesequence_apr22.py"),
    ("2026-04-23", "send_bytebytego_apr23.py"),
    ("2026-04-24", "send_systemdesign_apr24.py"),  # System Design Newsletter — Neo Kim, 227K subs
    ("2026-04-25", "send_mcplink_anyisalin_mar27.py"),  # mcp-link (605 stars) — agent-friend quality gate angle
]


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open("/home/agent/company/products/content/staggered.log", "a") as f:
        f.write(line + "\n")


def already_fired(script):
    if not FIRED_LOG.exists():
        return False
    return script in FIRED_LOG.read_text()


def mark_fired(script):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with open(FIRED_LOG, "a") as f:
        f.write(f"{ts} {script}\n")


def run_script(script_name):
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        log(f"Script not found: {script_name}")
        return

    result = subprocess.run(
        ["python3", str(script_path)],
        capture_output=True, text=True, timeout=120,
        input=None  # non-interactive
    )
    log(f"Ran {script_name} → RC={result.returncode}")
    if result.stdout:
        log(f"  STDOUT: {result.stdout[:300]}")
    if result.stderr:
        log(f"  STDERR: {result.stderr[:200]}")


def main():
    log("Outreach scheduler started")

    while True:
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

        for scheduled_date, script in SCHEDULE:
            if today >= scheduled_date and not already_fired(script):
                log(f"Firing {script} (scheduled {scheduled_date})")
                run_script(script)
                mark_fired(script)

        # Check once per hour
        time.sleep(3600)


if __name__ == "__main__":
    main()
