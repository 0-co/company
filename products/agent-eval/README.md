# agent-eval

AI agents fail silently. There's no standard way to test them.

89% of teams have observability. 52% run evals. That gap is where silent regressions live.

agent-eval is a minimal evaluation harness. Define test cases with inputs and expected outputs, run them against any agent function, get pass/fail/score results. It works like unit tests, but for agent behavior.

Zero dependencies. Pure stdlib. Python 3.9+.

---

## When you need this

- **Prompt regression testing** — changed your system prompt and want to make sure existing cases still pass before deploying
- **CI/CD LLM quality gate** — `results.assert_all_passed()` raises on failure with a non-zero exit code; drop it in your pipeline
- **Output format validation** — confirm your agent always returns JSON, or always includes required fields
- **A/B testing prompts** — run both prompt variants against the same eval suite, compare scores
- **Catching hallucinations** — assert the agent response contains (or doesn't contain) specific facts
- **Agent framework agnostic** — any `fn(str) -> str` works; wraps LangChain, CrewAI, AutoGen, or plain API calls the same way

---

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-eval
```

---

## Quick start

```python
from agent_eval import Case, Eval, EvalFailed

e = Eval()
e.add(Case("What is 2+2?", expected="4", scorer="exact"))
e.add(Case("Capital of France?", expected="Paris", scorer="contains"))
e.add(Case("Is water wet?", expected=r"yes|wet", scorer="regex"))

results = e.run(my_agent_fn)
print(results.summary())
# Runs: 3 | Passed: 3 | Failed: 0 | Score: 100.0%
#   [+] What is 2+2?
#   [+] Capital of France?
#   [+] Is water wet?

# CI integration: raises EvalFailed (non-zero exit) if any case fails
results.assert_all_passed()
```

`my_agent_fn` is any callable that takes a `str` and returns a `str`.

---

## Scorer types

### `"exact"` — strip and compare

```python
Case("What is 2+2?", expected="4", scorer="exact")
# passes if output.strip() == "4"
```

### `"contains"` — case-insensitive substring

```python
Case("Capital of France?", expected="Paris", scorer="contains")
# passes if "paris" in output.lower()
```

### `"regex"` — re.search, case-insensitive

```python
Case("Is water wet?", expected=r"yes|wet", scorer="regex")
# passes if re.search(r"yes|wet", output, IGNORECASE) matches
```

### `None` — always passes (baseline)

```python
Case("Any output works", scorer=None)
# always passes, score=1.0. Useful as a smoke test.
```

### Custom callable

```python
def concise(inp, out, exp):
    return len(out) < 500

Case("Summarize this", scorer=concise)

# Or inline:
Case("Summarize", expected="key point",
     scorer=lambda i, o, e: e.lower() in o.lower() and len(o) < 500)
```

Callable signature: `(input: str, output: str, expected: str | None) -> bool | float`

Return a `bool` (coerced to 0.0/1.0) or a `float` in [0.0, 1.0].

---

## CI integration

```python
results = eval.run(agent)
results.assert_all_passed()   # raises EvalFailed if any failed
```

`EvalFailed` inherits from `Exception`. In a script, an uncaught exception exits with code 1. To be explicit:

```python
import sys
from agent_eval import EvalFailed

try:
    results.assert_all_passed()
except EvalFailed as exc:
    print(f"FAILED: {exc}", file=sys.stderr)
    sys.exit(1)
```

---

## Timeouts

```python
Case("Slow query", expected="done", scorer="contains", timeout=5.0)
# fails if agent_fn takes more than 5 seconds
```

Timeout is implemented with a daemon thread. The agent call runs in the thread; if it hasn't returned within `timeout` seconds, the run is marked failed with a `TimeoutError` message in `error`.

---

## API reference

### `Case`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `input` | str | required | Passed to agent_fn |
| `expected` | str or None | None | Expected output for built-in scorers |
| `scorer` | str, callable, or None | None | How to score the output |
| `label` | str or None | None | Display name in summary output |
| `timeout` | float or None | None | Per-case timeout in seconds |

### `Eval`

```python
e = Eval()
e.add(case)          # returns self for chaining
e.run(agent_fn)      # returns EvalResults
e.cases              # list of registered Case objects
```

### `run()` — standalone function

```python
from agent_eval import run, Case

results = run(agent_fn, [
    Case("2+2?", expected="4", scorer="exact"),
    Case("Paris?", expected="France", scorer="contains"),
])
```

### `EvalResults`

| Attribute/Method | Type | Description |
|---|---|---|
| `.score` | float | Mean score across all runs (0.0–1.0) |
| `.passed` | int | Count where passed=True |
| `.failed` | int | Count where passed=False |
| `.total` | int | Total runs |
| `.summary(verbose=True)` | str | Formatted summary string |
| `.assert_all_passed()` | None | Raises EvalFailed if any failed |
| `iter(results)` | RunResult | Iterate over individual results |
| `len(results)` | int | Total run count |

### `RunResult`

```python
for r in results:
    print(r.case.input)    # the input string
    print(r.output)        # agent output (None if agent raised)
    print(r.passed)        # bool
    print(r.score)         # float 0.0–1.0
    print(r.error)         # exception message or None
    print(r.duration_ms)   # wall time in milliseconds
```

### `EvalFailed`

```python
except EvalFailed as exc:
    print(exc.failed_count)   # int — number of failed cases
    print(exc.total_count)    # int — total cases run
    print(exc.results)        # EvalResults — full result set
```

---

## How it works

Each `Case` is a tuple of (input, expected, scorer). When you call `e.run(agent_fn)`, the harness:

1. Calls `agent_fn(case.input)` in isolation (exceptions caught per-case)
2. Passes the output to the scorer
3. Records `RunResult(case, output, passed, score, error, duration_ms)`
4. Returns `EvalResults` wrapping all `RunResult` objects

No network calls. No state between runs. No global setup. Each run is independent.

The only threading is for timeout enforcement: if `case.timeout` is set, the agent call runs in a daemon thread and is abandoned (not killed — Python threads can't be forcibly killed) if it exceeds the limit. The run is marked failed and other cases continue.

---

## Why not use pytest?

pytest tests synchronous functions against known outputs. That works well when you control the output.

Agent outputs are non-deterministic. A factual answer can be correct without matching exactly. Format constraints, length limits, and semantic checks require flexible scoring. agent-eval handles that without fighting pytest's assertion model.

Use both: pytest for your infrastructure code, agent-eval for your agent behavior.

---

Built at [0co](https://github.com/0-co/company) — an AI autonomously running a startup.
