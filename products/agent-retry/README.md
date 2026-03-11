# agent-retry

AI agents fail constantly. Network timeouts, 429 rate limits, transient 500s. Most code either crashes silently or wraps every call in a hand-rolled `while True` loop.

agent-retry is retry logic designed for AI agent workflows: exponential backoff with jitter, `Retry-After` header awareness, sync and async support, zero dependencies.

```python
from agent_retry import retry

@retry(max_attempts=3, base_delay=1.0)
def call_claude():
    return client.messages.create(model="claude-opus-4-6", ...)
```

Zero dependencies. Pure stdlib. Python 3.9+.

---

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-retry
```

---

## Quick start

### Decorator

```python
from agent_retry import retry

# Defaults: 3 attempts, 1s base delay, exponential backoff, jitter
@retry
def call_api():
    return requests.get("https://api.example.com/data")

# Explicit configuration
@retry(max_attempts=5, base_delay=2.0, max_delay=30.0)
def call_openai():
    return openai_client.chat.completions.create(...)

# Async works identically
@retry(max_attempts=3)
async def async_call():
    return await async_client.messages.create(...)
```

### RetryConfig

```python
from agent_retry import retry, RetryConfig

config = RetryConfig(
    max_attempts=5,
    base_delay=1.0,
    max_delay=60.0,
    exponential_base=2.0,  # delays: 1s, 2s, 4s, 8s...
    jitter=True,           # randomise to avoid thundering herd
    on_retry=lambda attempt, exc, delay: print(f"Retry {attempt} in {delay:.1f}s: {exc}"),
    on_failure=lambda attempts, exc: print(f"Gave up after {attempts} attempts"),
)

@retry(config=config)
def call_with_logging():
    ...
```

### Retryable exceptions and status codes

```python
from agent_retry import retry

# Only retry on specific exceptions
@retry(
    max_attempts=4,
    retryable_exceptions=(ConnectionError, TimeoutError),
)
def network_call():
    ...

# By HTTP status code (checks exc.status_code, exc.response.status_code)
@retry(
    max_attempts=3,
    retryable_status_codes=(429, 503),
)
def rate_limited_api():
    ...

# Non-retryable exceptions pass through immediately, unchanged
```

### Retry-After awareness

If the exception has a `Retry-After` value (checked in `exc.retry_after`,
`exc.headers["Retry-After"]`, or `exc.response.headers["Retry-After"]`),
agent-retry uses that delay instead of computing one.

Most rate-limit clients from Anthropic, OpenAI, and similar SDKs expose this
automatically — agent-retry picks it up with no extra configuration.

```python
@retry(max_attempts=5)  # Respects Retry-After if present
def call_claude():
    return anthropic_client.messages.create(...)
```

---

## LLM error classification

agent-retry knows which LLM errors are retryable and which aren't.

**Retried by default** (transient — the server failed, not your request):

| Code | Meaning |
|------|---------|
| 429 | Rate limited — wait and retry |
| 529 | Anthropic overloaded — wait and retry |
| 500 | Server error — might work next time |
| 502, 503, 504 | Gateway/service unavailable |

**Never retried by default** (fatal — your request is wrong):

| Code | Meaning |
|------|---------|
| 400 | Bad request, including `context_length_exceeded` — retrying wastes tokens |
| 401 | Unauthorized — fix your API key first |
| 403 | Forbidden — retrying won't fix permissions |
| 413 | Payload too large — shrink your prompt |

This is the key difference from generic libraries like `tenacity`. Tenacity retries everything unless you configure it explicitly. agent-retry knows the difference between "try again later" and "this will never work."

To override:

```python
@retry(
    retryable_status_codes=(429, 529),   # only rate limits
    non_retryable_status_codes=(400,),   # still block 400
)
def call_claude(): ...
```

---

## RetryConfig reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_attempts` | int | 3 | Total attempts (1 = no retries) |
| `base_delay` | float | 1.0 | Seconds before first retry |
| `max_delay` | float | 60.0 | Upper bound on delay |
| `exponential_base` | float | 2.0 | Backoff multiplier |
| `jitter` | bool | True | Uniform random jitter in [0, delay] |
| `retryable_exceptions` | tuple | `(Exception,)` | Exception types to retry |
| `retryable_status_codes` | tuple | `(429, 529, 500, 502, 503, 504)` | Status codes to retry |
| `non_retryable_status_codes` | tuple | `(400, 401, 403, 413)` | Status codes never retried (checked first) |
| `on_retry` | callable | None | Called before each retry `(attempt, exc, delay)` |
| `on_failure` | callable | None | Called on final failure `(attempts, exc)` |

---

## RetryExhausted

When all attempts are exhausted, `RetryExhausted` is raised:

```python
from agent_retry import retry, RetryExhausted

@retry(max_attempts=3)
def unreliable():
    raise ConnectionError("down")

try:
    unreliable()
except RetryExhausted as e:
    print(e.attempts)         # 3
    print(e.last_exception)   # ConnectionError('down')
```

Non-retryable exceptions are **not** wrapped — they pass through as-is.

---

## Pairs with agent-budget

Use agent-budget to enforce cost limits, agent-retry to handle transient failures:

```python
from agent_budget import BudgetClient
from agent_retry import retry

client = BudgetClient(anthropic_client, max_cost_usd=5.0)

@retry(max_attempts=3, retryable_status_codes=(429,))
def call_claude(prompt: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
```

---

## How it works

Pure function decorator. No global state. Each decorated function gets its own
retry loop. Works with any callable — no SDK-specific integrations needed.

Delay formula: `min(base_delay * exponential_base ** (attempt - 1), max_delay)`.
With jitter: `uniform(0, delay)`. Non-retryable exceptions bypass the loop entirely.

---

Built at [0co](https://github.com/0-co/company) — an AI autonomously running a startup.
