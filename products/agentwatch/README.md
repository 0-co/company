# AgentWatch

**Detect silent exit-0 failures and behavioral drift in AI agent runs.**

## The Problem

AI agents lie. Not intentionally — but they exit 0 and print "Done" while the task quietly failed: the database has 0 new rows, the PDF was never written, the API call was swallowed by a try/except, and the output file is missing. Nobody notices until a user reports it two days later. AgentWatch wraps your agent invocation with a post-run verification check and tracks pass rates over time, so you catch silent failures immediately and spot behavioral drift before it becomes an incident.

---

## Example Use Cases

### 1. Order Processing Agent
An agent processes orders from a queue and writes them to a database. Verify that new rows actually appeared:

```bash
python3 agentwatch.py run \
  --cmd "python3 order_agent.py --queue orders" \
  --verify "python3 -c \"import sqlite3; c=sqlite3.connect('orders.db'); print(c.execute('SELECT COUNT(*) FROM orders').fetchone()[0]); exit(0 if c.execute('SELECT COUNT(*) FROM orders').fetchone()[0] > 0 else 1)\"" \
  --session "order_processor"
```

If the agent exits 0 but the DB has 0 rows, AgentWatch flags it:
```
  WARNING  Silent exit-0 failure detected
           Agent reported success (exit 0) but verification failed.
```

### 2. Report Generation Agent
An agent generates a PDF report nightly. Verify the file was created and is non-empty:

```bash
python3 agentwatch.py run \
  --cmd "python3 report_agent.py --date today" \
  --verify "/output/report.pdf" \
  --verify-type file \
  --session "report_generator"
```

### 3. Data Pipeline Agent
An agent downloads and transforms data, writing results to a CSV. Verify the output is non-empty:

```bash
python3 agentwatch.py run \
  --cmd "python3 pipeline.py --source s3://bucket/raw/" \
  --verify "/data/output/transformed.csv" \
  --verify-type file \
  --session "data_pipeline"
```

Then check drift over time:
```bash
python3 agentwatch.py report --session "data_pipeline"
# =>  WARNING  Behavioral drift detected: 62% success rate
```

---

## Quick Start

No install required — AgentWatch is a single stdlib-only Python file.

```bash
# 1. Download
curl -O https://raw.githubusercontent.com/0-co/company/master/products/agentwatch/agentwatch.py

# 2. Run your first check
python3 agentwatch.py check --verify "test -f /etc/hostname" --session "smoke_test"
```

---

## CLI Reference

### `run` — Execute agent and verify

```bash
python3 agentwatch.py run \
  --cmd "python3 my_agent.py" \
  --verify "test -f /output/report.pdf" \
  --session "report_generator" \
  [--verify-type shell|file|http] \
  [--expect 200] \
  [--webhook https://discord.com/api/webhooks/...]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--cmd` | Yes | Shell command to run your agent |
| `--verify` | Yes | Verification: shell cmd, file path, or URL |
| `--session` | Yes | Session name for grouping runs |
| `--verify-type` | No | `shell` (default), `file`, or `http` |
| `--expect` | No | Expected HTTP status for `--verify-type http` (default: 200) |
| `--webhook` | No | URL to POST JSON alert to on failure |

### `check` — Verify state without running

```bash
python3 agentwatch.py check \
  --verify "test -f /output/report.pdf" \
  --session "report_generator" \
  [--verify-type shell|file|http] \
  [--expect 200] \
  [--webhook https://...]
```

Use this after an agent has already run, or to spot-check current state.

### `report` — Drift analysis for a session

```bash
python3 agentwatch.py report --session "report_generator"
```

Shows: total runs, pass rate, recent vs. previous trend, last 10 runs table.
Alerts if pass rate drops below 80%:
```
  WARNING  Behavioral drift detected: 62% success rate
```

### `list` — All sessions at a glance

```bash
python3 agentwatch.py list
```

Shows every session with run count and pass rate. Sessions below 80% are flagged `[drift]`.

---

## Verification Types

| Type | `--verify` value | Passes when |
|------|-----------------|-------------|
| `shell` (default) | Any shell command | Exit code 0 |
| `file` | File path | File exists AND is non-empty |
| `http` | URL | HTTP status == `--expect` (default 200) |

### Examples

```bash
# Shell: count rows in SQLite
--verify "sqlite3 orders.db 'SELECT COUNT(*) FROM orders WHERE date=date(\"now\")' | grep -v '^0$'"

# File: PDF was written
--verify "/output/report.pdf" --verify-type file

# HTTP: API is up after agent deployed it
--verify "https://api.myapp.com/health" --verify-type http --expect 200
```

---

## Webhook Alerts (Discord / Slack)

Pass `--webhook URL` on `run` or `check` to get a POST when a check fails:

```bash
python3 agentwatch.py run \
  --cmd "python3 agent.py" \
  --verify "test -f output.csv" \
  --session "daily_pipeline" \
  --webhook "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/TOKEN"
```

Payload sent on failure:
```json
{
  "session": "daily_pipeline",
  "failed_check": "test -f output.csv",
  "ts": "2026-03-09T12:00:00+00:00"
}
```

---

## Data Storage

Runs are stored in `.agentwatch/{session_name}.jsonl` relative to your working directory. Each line is one run:

```json
{"ts": "2026-03-09T12:00:00+00:00", "passed": false, "verify_cmd": "test -f output.pdf", "verify_type": "shell", "duration_ms": 4821, "agent_exit_code": 0, "detail": ""}
```

---

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)

---

## Beta Waitlist

AgentWatch is part of the AgentWatch reliability monitoring platform — dashboards, multi-check pipelines, team alerting, and more.

**Join the beta waitlist:** https://github.com/0-co/company/issues/6
