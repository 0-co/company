#!/usr/bin/env python3
"""
AgentWatch v0.1 — Detect silent exit-0 failures and behavioral drift in AI agent runs.

Usage:
  python3 agentwatch.py run --cmd "python3 agent.py" --verify "test -f output.pdf" --session "my_agent"
  python3 agentwatch.py check --verify "test -f output.pdf" --session "my_agent"
  python3 agentwatch.py report --session "my_agent"
  python3 agentwatch.py list
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


# ─── Storage ───────────────────────────────────────────────────────────────────

STORE_DIR = ".agentwatch"


def get_session_path(session: str) -> Path:
    store = Path(STORE_DIR)
    store.mkdir(exist_ok=True)
    return store / f"{session}.jsonl"


def append_run(session: str, record: dict) -> None:
    path = get_session_path(session)
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


def load_runs(session: str, limit: int = 30) -> list:
    path = get_session_path(session)
    if not path.exists():
        return []
    lines = path.read_text().strip().splitlines()
    records = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records[-limit:]


def list_sessions() -> list:
    store = Path(STORE_DIR)
    if not store.exists():
        return []
    sessions = []
    for f in sorted(store.glob("*.jsonl")):
        name = f.stem
        runs = load_runs(name, limit=10000)
        if runs:
            passed = sum(1 for r in runs if r.get("passed"))
            rate = int(passed / len(runs) * 100) if runs else 0
            sessions.append({"name": name, "runs": len(runs), "pass_rate": rate})
    return sessions


# ─── Verification ──────────────────────────────────────────────────────────────

def run_shell_verify(cmd: str) -> tuple:
    """Run a shell command verification. Returns (passed, detail)."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
        passed = result.returncode == 0
        detail = result.stderr.decode().strip() or result.stdout.decode().strip()
        return passed, detail
    except subprocess.TimeoutExpired:
        return False, "Verification timed out after 30s"
    except Exception as e:
        return False, f"Verification error: {e}"


def run_file_verify(path_str: str) -> tuple:
    """Check file exists and is non-empty. Returns (passed, detail)."""
    p = Path(path_str)
    if not p.exists():
        return False, f"File does not exist: {path_str}"
    if p.stat().st_size == 0:
        return False, f"File exists but is empty: {path_str}"
    return True, f"File OK: {path_str} ({p.stat().st_size} bytes)"


def run_http_verify(url: str, expect_status: int = 200) -> tuple:
    """GET url and check status code. Returns (passed, detail)."""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            passed = status == expect_status
            return passed, f"HTTP {status} (expected {expect_status})"
    except urllib.error.HTTPError as e:
        passed = e.code == expect_status
        return passed, f"HTTP {e.code} (expected {expect_status})"
    except Exception as e:
        return False, f"HTTP request failed: {e}"


def run_verification(verify: str, verify_type: str, expect: int = 200) -> tuple:
    """Dispatch to the appropriate verification method. Returns (passed, detail)."""
    if verify_type == "shell":
        return run_shell_verify(verify)
    elif verify_type == "file":
        return run_file_verify(verify)
    elif verify_type == "http":
        return run_http_verify(verify, expect_status=expect)
    else:
        return False, f"Unknown verify type: {verify_type}"


# ─── Webhook ───────────────────────────────────────────────────────────────────

def post_webhook(url: str, session: str, failed_check: str, ts: str) -> None:
    payload = json.dumps({
        "session": session,
        "failed_check": failed_check,
        "ts": ts,
    }).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            pass  # success
    except Exception as e:
        print(f"  [webhook] Warning: POST to {url} failed: {e}", file=sys.stderr)


# ─── Commands ──────────────────────────────────────────────────────────────────

def cmd_run(args) -> int:
    print(f"[agentwatch] Running agent: {args.cmd}")
    start = time.monotonic()
    ts = datetime.now(timezone.utc).isoformat()

    # Execute the agent command
    try:
        proc = subprocess.run(
            args.cmd,
            shell=True,
            stdout=None,   # inherit: let agent output flow to terminal
            stderr=None,
        )
        agent_exit_code = proc.returncode
    except Exception as e:
        print(f"[agentwatch] Failed to run command: {e}", file=sys.stderr)
        return 1

    duration_ms = int((time.monotonic() - start) * 1000)
    print(f"[agentwatch] Agent exited with code {agent_exit_code} in {duration_ms}ms")

    # Run verification
    verify_type = args.verify_type if hasattr(args, "verify_type") else "shell"
    expect = args.expect if hasattr(args, "expect") else 200
    print(f"[agentwatch] Verifying [{verify_type}]: {args.verify}")
    passed, detail = run_verification(args.verify, verify_type, expect)

    record = {
        "ts": ts,
        "passed": passed,
        "verify_cmd": args.verify,
        "verify_type": verify_type,
        "duration_ms": duration_ms,
        "agent_exit_code": agent_exit_code,
        "detail": detail,
    }
    append_run(args.session, record)

    # Print result
    if passed:
        print(f"\n  PASS  Verification passed")
        if detail:
            print(f"        {detail}")
    else:
        print(f"\n  FAIL  Verification failed")
        if detail:
            print(f"        {detail}")
        if agent_exit_code == 0:
            print(f"\n  WARNING  Silent exit-0 failure detected")
            print(f"        Agent reported success (exit 0) but verification failed.")
            print(f"        Check your agent logic — it may be swallowing errors.")
        # Webhook alert
        if args.webhook:
            post_webhook(args.webhook, args.session, args.verify, ts)
            print(f"  [webhook] Alert posted to {args.webhook}")

    print(f"\n  Session '{args.session}' logged to {get_session_path(args.session)}")
    print(f"  Run 'python3 agentwatch.py report --session {args.session}' to view history.")
    return 0 if passed else 1


def cmd_check(args) -> int:
    ts = datetime.now(timezone.utc).isoformat()
    verify_type = args.verify_type if hasattr(args, "verify_type") else "shell"
    expect = args.expect if hasattr(args, "expect") else 200
    print(f"[agentwatch] Checking [{verify_type}]: {args.verify}")
    passed, detail = run_verification(args.verify, verify_type, expect)

    record = {
        "ts": ts,
        "passed": passed,
        "verify_cmd": args.verify,
        "verify_type": verify_type,
        "duration_ms": 0,
        "agent_exit_code": None,
        "detail": detail,
    }
    append_run(args.session, record)

    if passed:
        print(f"\n  PASS  Check passed")
        if detail:
            print(f"        {detail}")
    else:
        print(f"\n  FAIL  Check failed")
        if detail:
            print(f"        {detail}")
        print(f"\n  Hint: Add more checks with:")
        print(f"        python3 agentwatch.py check --verify \"<your check>\" --session {args.session}")
        if args.webhook:
            post_webhook(args.webhook, args.session, args.verify, ts)
            print(f"  [webhook] Alert posted to {args.webhook}")

    print(f"\n  Session '{args.session}' logged to {get_session_path(args.session)}")
    return 0 if passed else 1


def cmd_report(args) -> int:
    runs = load_runs(args.session, limit=30)
    if not runs:
        print(f"[agentwatch] No runs found for session '{args.session}'.")
        print(f"  Start recording with:")
        print(f"    python3 agentwatch.py run --cmd \"your_agent\" --verify \"test -f output\" --session {args.session}")
        return 0

    total = len(runs)
    passed_count = sum(1 for r in runs if r.get("passed"))
    pass_rate = int(passed_count / total * 100) if total else 0

    # Trend: last 5 vs previous 5
    recent = runs[-5:]
    previous = runs[-10:-5] if len(runs) >= 10 else []
    recent_rate = int(sum(1 for r in recent if r.get("passed")) / len(recent) * 100) if recent else 0
    prev_rate = int(sum(1 for r in previous if r.get("passed")) / len(previous) * 100) if previous else None

    print(f"\n=== AgentWatch Report: '{args.session}' ===\n")
    print(f"  Total runs  : {total}")
    print(f"  Pass rate   : {pass_rate}%  ({passed_count}/{total})")

    if prev_rate is not None:
        arrow = "up" if recent_rate > prev_rate else ("down" if recent_rate < prev_rate else "stable")
        print(f"  Trend       : last 5 = {recent_rate}%, prev 5 = {prev_rate}% ({arrow})")
    else:
        print(f"  Trend       : last 5 = {recent_rate}%  (not enough history for trend)")

    if pass_rate < 80:
        print(f"\n  WARNING  Behavioral drift detected: {pass_rate}% success rate")
        print(f"           Your agent is failing more than 20% of the time.")
        print(f"           Check agent logs and verify logic for session '{args.session}'.")

    # Last 10 runs table
    last10 = runs[-10:]
    print(f"\n  Last {len(last10)} runs:")
    print(f"  {'#':<4} {'Timestamp':<28} {'Result':<8} {'Exit':<6} {'Duration':<12} {'Verify'}")
    print(f"  {'-'*4} {'-'*28} {'-'*8} {'-'*6} {'-'*12} {'-'*30}")
    for i, r in enumerate(last10, start=max(1, total - len(last10) + 1)):
        ts = r.get("ts", "?")[:19].replace("T", " ")
        result = "PASS" if r.get("passed") else "FAIL"
        exit_code = str(r.get("agent_exit_code", "-"))
        dur = f"{r.get('duration_ms', 0)}ms"
        verify = r.get("verify_cmd", "?")
        if len(verify) > 35:
            verify = verify[:32] + "..."
        print(f"  {i:<4} {ts:<28} {result:<8} {exit_code:<6} {dur:<12} {verify}")

    print()
    return 0


def cmd_list(args) -> int:
    sessions = list_sessions()
    if not sessions:
        store = Path(STORE_DIR)
        print(f"[agentwatch] No sessions found in {store.resolve()}/")
        print(f"  Start your first session with:")
        print(f"    python3 agentwatch.py run --cmd \"your_agent\" --verify \"test -f output\" --session my_agent")
        return 0

    print(f"\n=== AgentWatch Sessions ===\n")
    print(f"  {'Session':<30} {'Runs':<8} {'Pass Rate'}")
    print(f"  {'-'*30} {'-'*8} {'-'*10}")
    for s in sessions:
        rate_str = f"{s['pass_rate']}%"
        drift = "  [drift]" if s["pass_rate"] < 80 else ""
        print(f"  {s['name']:<30} {s['runs']:<8} {rate_str}{drift}")
    print()
    print(f"  Run 'python3 agentwatch.py report --session <name>' for details.")
    return 0


# ─── Argument parsing ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentwatch",
        description="Detect silent exit-0 failures and behavioral drift in AI agent runs.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # run
    p_run = sub.add_parser("run", help="Run an agent command and verify the result")
    p_run.add_argument("--cmd", required=True, help="Agent command to execute")
    p_run.add_argument("--verify", required=True, help="Verification command/path/URL")
    p_run.add_argument(
        "--verify-type",
        dest="verify_type",
        choices=["shell", "file", "http"],
        default="shell",
        help="Verification type: shell (default), file, or http",
    )
    p_run.add_argument("--session", required=True, help="Session name (used for grouping runs)")
    p_run.add_argument(
        "--expect",
        type=int,
        default=200,
        help="Expected HTTP status code (for --verify-type http, default: 200)",
    )
    p_run.add_argument("--webhook", default=None, help="Webhook URL to POST alert if check fails")

    # check
    p_check = sub.add_parser("check", help="Verify state without running an agent")
    p_check.add_argument("--verify", required=True, help="Verification command/path/URL")
    p_check.add_argument(
        "--verify-type",
        dest="verify_type",
        choices=["shell", "file", "http"],
        default="shell",
        help="Verification type: shell (default), file, or http",
    )
    p_check.add_argument("--session", required=True, help="Session name")
    p_check.add_argument(
        "--expect",
        type=int,
        default=200,
        help="Expected HTTP status code (for --verify-type http, default: 200)",
    )
    p_check.add_argument("--webhook", default=None, help="Webhook URL to POST alert if check fails")

    # report
    p_report = sub.add_parser("report", help="View history and drift analysis for a session")
    p_report.add_argument("--session", required=True, help="Session name")

    # list
    sub.add_parser("list", help="List all sessions with run count and pass rate")

    return parser


# ─── Entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "run": cmd_run,
        "check": cmd_check,
        "report": cmd_report,
        "list": cmd_list,
    }
    fn = dispatch.get(args.command)
    if fn is None:
        parser.print_help()
        return 1
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
