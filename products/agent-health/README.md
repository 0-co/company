# agent-health

Health checks for AI APIs. Know before your agents do.

```python
from agent_health import HealthChecker, AnthropicProbe

checker = HealthChecker(AnthropicProbe(client))
result = checker.check()
print(result.status)   # HealthStatus.UP
print(result.latency_ms)  # 127.3
```

Zero dependencies. Works with Anthropic, OpenAI, or any custom endpoint.

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-health
```

## When you need this

Your agents call AI APIs hundreds of times. When those APIs are slow or down, your agents don't know it until they're already hanging or throwing exceptions. By then, you've wasted tokens, time, and compute on a dead endpoint.

`agent-health` gives you a lightweight probe layer: run checks before calls, watch in the background, gate functions on health status, and pick the fastest healthy provider when you have multiple.

Pairs naturally with [agent-fallback](../agent-fallback) — use a `HealthPool` to pick healthy providers instead of waiting for errors to trigger circuit breakers.

## Status values

| Status | Meaning |
|--------|---------|
| `UP` | Probe succeeded within latency thresholds |
| `DEGRADED` | Probe succeeded but latency was high |
| `DOWN` | Probe failed (exception raised) |
| `UNKNOWN` | No checks have run yet |

`DEGRADED` is still considered healthy — `is_healthy` returns `True` for both `UP` and `DEGRADED`.

## Core API

### `HealthChecker`

```python
from agent_health import HealthChecker, AnthropicProbe, OpenAIProbe, CustomProbe

# Anthropic
probe = AnthropicProbe(anthropic_client)
checker = HealthChecker(probe, degraded_threshold_ms=3000)

# OpenAI
probe = OpenAIProbe(openai_client)
checker = HealthChecker(probe)

# Any callable
probe = CustomProbe(lambda: requests.get("https://api.example.com/health").raise_for_status())
checker = HealthChecker(probe)
```

**One-shot check:**
```python
result = checker.check()
result.status        # HealthStatus.UP / DEGRADED / DOWN
result.latency_ms    # 127.3
result.error         # None or "Connection refused"
result.is_healthy    # True if UP or DEGRADED
```

**Status and history:**
```python
checker.status          # latest status (UNKNOWN if no checks yet)
checker.is_healthy      # True if UP or DEGRADED
checker.latest          # most recent HealthResult
checker.history         # list of all results (copy)
checker.success_rate()          # fraction of healthy checks
checker.success_rate(last_n=10) # over last 10 checks
checker.average_latency_ms()    # average latency
checker.p95_latency_ms()        # 95th percentile latency
```

**Background polling:**
```python
def on_status_change(checker, result):
    print(f"Status changed to {result.status}")

checker.start_watching(interval=30, on_status_change=on_status_change)
# ... your app runs ...
print(checker.status)  # always current
checker.stop_watching()
```

**Gate calls on health:**
```python
@checker.requires_healthy
def call_api(prompt):
    return client.messages.create(...)

# Raises RuntimeError if checker is DOWN
# If status is UNKNOWN, runs one probe first
result = call_api("hello")
```

### `HealthPool`

Manage multiple providers. Pairs with `agent-fallback` for smart routing.

```python
from agent_health import HealthPool, HealthChecker, AnthropicProbe, OpenAIProbe

pool = HealthPool({
    "anthropic": HealthChecker(AnthropicProbe(anthropic_client), name="anthropic"),
    "openai":    HealthChecker(OpenAIProbe(openai_client),    name="openai"),
})

# Check all providers
results = pool.check_all()   # {"anthropic": HealthResult(...), "openai": HealthResult(...)}

# Query health
pool.healthy()       # ["anthropic", "openai"]  — UP or DEGRADED
pool.up()            # ["anthropic"]              — strictly UP
pool.down()          # []                         — DOWN only
pool.any_healthy()   # True
pool.all_healthy()   # True

# Best provider (fastest UP, then DEGRADED, then None)
name = pool.best()   # "anthropic"

# Summary for logging
pool.summary()
# {
#   "total": 2, "up": 2, "degraded": 0, "down": 0,
#   "any_healthy": True, "best": "anthropic",
#   "statuses": {"anthropic": "up", "openai": "up"}
# }

# Background watching
pool.start_watching_all(interval=30)
pool.stop_watching_all()
```

## Integration with agent-fallback

```python
from agent_health import HealthPool, HealthChecker, AnthropicProbe, OpenAIProbe

pool = HealthPool({
    "anthropic": HealthChecker(AnthropicProbe(anthropic_client)),
    "openai":    HealthChecker(OpenAIProbe(openai_client)),
})
pool.start_watching_all(interval=30)

def call_best_provider(prompt):
    provider_name = pool.best()
    if not provider_name:
        raise RuntimeError("All providers are DOWN")
    client = clients[provider_name]
    return client.messages.create(...)
```

## Custom probes

Any callable that returns `(success: bool, latency_ms: float, error: str | None)`:

```python
from agent_health import CustomProbe, HealthChecker

def my_probe():
    start = time.monotonic()
    try:
        response = requests.get("https://api.example.com/v1/ping", timeout=5)
        response.raise_for_status()
        return True, (time.monotonic() - start) * 1000, None
    except Exception as e:
        return False, (time.monotonic() - start) * 1000, str(e)

checker = HealthChecker(my_probe)
```

Or subclass `Probe`:

```python
from agent_health import Probe

class MyProbe(Probe):
    def __init__(self, client):
        self.client = client

    def _execute(self):
        # Raise on failure. Latency is measured automatically.
        self.client.ping()

checker = HealthChecker(MyProbe(client))
```

## Reliability suite

`agent-health` is part of a zero-dependency Python reliability toolkit for AI agents:

- [agent-retry](../agent-retry) — exponential backoff for API calls
- [agent-timeout](../agent-timeout) — deadline enforcement
- [agent-fallback](../agent-fallback) — multi-provider failover with circuit breakers
- **agent-health** — health checks and probes ← you are here

## Tests

```bash
python3 -m unittest tests.test_health -v
# 77 tests in ~1s
```

---

Built by [0co](https://0-co.github.io/company/) — an AI-operated company, live on Twitch.
