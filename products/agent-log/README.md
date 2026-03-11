# agent-log — structured logging for AI agents

Zero-dependency structured logging built for AI agent workflows.
Sessions, spans, token tracking, cost calculation, secret redaction. Python 3.8+.

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-log
```

---

## When you need this

Python's stdlib `logging` module was built for long-running servers, not multi-step agent runs.
Here is what it cannot do:

- **You have no way to correlate events across a run.** `logging` emits flat lines.
  If an agent calls an LLM three times and a tool twice, you cannot tell which log lines
  belong to the same task without stitching them together manually.

- **You want to track LLM calls, costs, and latency.** Span timing and token cost are
  not concepts that exist in `logging`. You end up writing the same boilerplate in every project.

- **You have accidentally logged an API key.** Agent code passes secrets through
  args dicts, result strings, and error messages. `agent-log` auto-redacts `sk-...`,
  `ghp_...`, `Bearer ...`, and any field whose name contains `SECRET`, `TOKEN`, `KEY`,
  or `PASSWORD` — before a single byte reaches disk.

- **You want JSON logs that feed into any aggregator without a new dependency.**
  Datadog, Grafana, ELK, CloudWatch — they all ingest JSONL. `agent-log` emits
  one JSON line per event and one summary line per session, with no third-party packages.

---

## Quick start

```python
from agent_log import AgentLogger

log = AgentLogger("my-agent")

with log.session(task="summarize docs") as session:
    session.info("Starting pipeline")

    with session.span("llm_call", model="claude-opus-4") as span:
        response = call_llm(prompt)
        span.tokens(prompt=500, completion=100, model="claude-opus-4")
        span.info("LLM responded", chars=len(response))

    session.tool_call(
        "read_file",
        args={"path": "/tmp/data.txt"},
        result_summary="3.2KB text",
        duration_ms=12,
    )

    session.decision("Will use the LLM output — quality looks acceptable")

# Session auto-emits a JSON summary on exit:
# {
#   "event": "session_end",
#   "session_id": "abc123...",
#   "agent": "my-agent",
#   "task": "summarize docs",
#   "duration_ms": 1234,
#   "spans": [{"name": "llm_call", "duration_ms": 800, "tokens": {...}, "cost_usd": 0.009}],
#   "tool_calls": [{"tool": "read_file", ...}],
#   "decisions": ["Will use the LLM output — quality looks acceptable"],
#   "total_tokens": {"prompt": 500, "completion": 100, "total": 600},
#   "total_cost_usd": 0.009,
#   "ts": "2026-03-11T17:30:01.000Z"
# }
```

---

## Output formats

### JSON (default) — one event per line (JSONL)

```python
log = AgentLogger("my-agent")                      # stdout, JSON
log = AgentLogger("my-agent", output="run.jsonl")  # file, JSON
```

```jsonl
{"event": "session_start", "session_id": "abc123", "agent": "my-agent", "task": "summarize docs", "ts": "2026-03-11T17:30:00.000Z"}
{"event": "info", "session_id": "abc123", "agent": "my-agent", "message": "Starting pipeline", "ts": "2026-03-11T17:30:00.010Z"}
{"event": "span_end", "session_id": "abc123", "agent": "my-agent", "span": "llm_call", "duration_ms": 800, "tokens": {"prompt": 500, "completion": 100, "total": 600}, "cost_usd": 0.009375, "ts": "2026-03-11T17:30:00.810Z"}
{"event": "tool_call", "session_id": "abc123", "agent": "my-agent", "tool": "read_file", "args": {"path": "/tmp/data.txt"}, "result_summary": "3.2KB text", "duration_ms": 12, "ts": "2026-03-11T17:30:00.822Z"}
{"event": "decision", "session_id": "abc123", "agent": "my-agent", "reasoning": "Will use the LLM output...", "ts": "2026-03-11T17:30:00.830Z"}
{"event": "session_end", "session_id": "abc123", "agent": "my-agent", "task": "summarize docs", "duration_ms": 1234, "spans": [...], "tool_calls": [...], "decisions": [...], "total_tokens": {"prompt": 500, "completion": 100, "total": 600}, "total_cost_usd": 0.009375, "ts": "2026-03-11T17:30:01.000Z"}
```

### Text — human-readable

```python
log = AgentLogger("my-agent", format="text")
```

```
[2026-03-11T17:30:00.000Z] [my-agent] [abc12345] SESSION START task=summarize docs
[2026-03-11T17:30:00.010Z] [my-agent] [abc12345] INFO Starting pipeline
[2026-03-11T17:30:00.810Z] [my-agent] [abc12345] SPAN llm_call duration=800ms tokens=600 cost=$0.009375
[2026-03-11T17:30:00.822Z] [my-agent] [abc12345] TOOL read_file 12ms
[2026-03-11T17:30:00.830Z] [my-agent] [abc12345] DECISION Will use the LLM output...
[2026-03-11T17:30:01.000Z] [my-agent] [abc12345] SESSION END duration=1234ms tokens=600 cost=$0.009375
```

---

## API reference

### AgentLogger

```python
AgentLogger(
    name: str,
    output: str | None = None,   # None = stdout, str = file path (append)
    level: str = "INFO",         # "DEBUG" | "INFO" | "WARNING" | "ERROR"
    format: str = "json",        # "json" | "text"
    redact: bool = True,         # auto-redact secrets
)
```

| Method | Description |
|---|---|
| `session(task=None, **metadata)` | Returns a `Session` context manager |
| `configure(output, level, format, redact)` | Update settings at runtime |
| `close()` | Flush and close output file |

---

### Session

Context manager. Each session gets a UUID4 `session_id`.

```python
with log.session(task="my task", run_id="42") as session:
    ...
```

| Method | Description |
|---|---|
| `info(message, **extra)` | Log an info event |
| `warning(message, **extra)` | Log a warning |
| `error(message, exc=None, **extra)` | Log an error, optionally attaching an exception |
| `span(name, **metadata)` | Create a child `Span` context manager |
| `tool_call(name, args=None, result_summary=None, duration_ms=None)` | Log a tool invocation |
| `decision(reasoning, **extra)` | Log an agent reasoning/decision step |

On `__exit__`, a `session_end` event is emitted with the full summary.

---

### Span

Context manager. Tracks duration automatically.

```python
with session.span("llm_call", model="gpt-4o") as span:
    response = call_api(...)
    span.tokens(prompt=500, completion=100, model="gpt-4o")
```

| Method | Description |
|---|---|
| `tokens(prompt=0, completion=0, model=None)` | Record token usage; calculates cost if model is known |
| `info(message, **extra)` | Log an event within this span |
| `error(message, exc=None, **extra)` | Log an error within this span |

On `__exit__`, a `span_end` event is emitted with duration, tokens, and cost.

---

### Token costs (hardcoded, zero deps)

| Model | Prompt (per 1M) | Completion (per 1M) |
|---|---|---|
| `claude-opus-4` | $15.00 | $75.00 |
| `claude-sonnet-4` | $3.00 | $15.00 |
| `claude-haiku-4` | $0.80 | $4.00 |
| `gpt-4o` | $2.50 | $10.00 |
| `gpt-4o-mini` | $0.15 | $0.60 |
| `gpt-4-turbo` | $10.00 | $30.00 |

Model name matching is prefix-based, so `claude-opus-4-20250514` resolves correctly.

---

## Configuration

```python
# Write to file instead of stdout
log = AgentLogger("my-agent", output="/var/log/agent/run.jsonl")

# Human-readable for local dev, JSON for production
import os
fmt = "text" if os.getenv("DEV") else "json"
log = AgentLogger("my-agent", format=fmt)

# Disable redaction (e.g. in a sandboxed test environment)
log = AgentLogger("my-agent", redact=False)

# Reconfigure at runtime
log.configure(output="/new/path.jsonl", format="json")
```

---

## Works with

- Python 3.8+ (no third-party dependencies)
- Any AI provider — Anthropic, OpenAI, Mistral, local models
- Any log aggregator that accepts JSONL — Datadog, Grafana Loki, ELK, CloudWatch

---

## agent-* suite

`agent-log` is part of a suite of zero-dependency Python libraries for production AI agents:

| Library | What it does |
|---|---|
| [agent-budget](../agent-budget/) | Enforce cost and token limits — raises `BudgetExceeded` before you overspend |
| [agent-context](../agent-context/) | Prevent context rot — sliding window, token budget, compress-middle strategies |
| [agent-eval](../agent-eval/) | Unit testing for agents — exact/contains/regex scorers, CI-friendly |
| [agent-shield](../agent-shield/) | Security scanner — prompt injection, credential theft, MCP config auditing |
| [agent-id](../agent-id/) | Identity and trust — HMAC tokens, trust registry, signed audit log |
| [agent-retry](../agent-retry/) | Exponential backoff — Retry-After aware, sync/async, non-retryable status codes |
| [agent-gate](../agent-gate/) | Human-in-the-loop approval — pause before irreversible actions |

Install any via:
```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-<name>
```
