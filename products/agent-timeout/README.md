# agent-timeout

Zero-dependency deadline and timeout enforcement for AI agent API calls.

## When you need this

- An LLM API call hangs indefinitely and your agent freezes
- An agentic loop stops making progress — no error, just silence
- You're retrying failed API calls and need to cap the total wall-clock time, not just per-call time
- You want to enforce timeouts in worker threads, background tasks, or non-main threads (where `signal.alarm` doesn't work)

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-timeout
```

Zero dependencies. Python 3.9+. Works on Linux, macOS, Windows.

## Quick start

### `with_timeout()` — wrap a callable

```python
from agent_timeout import with_timeout, TimeoutExceeded

try:
    result = with_timeout(30, anthropic_client.messages.create, **params)
except TimeoutExceeded as e:
    print(f"API call hung for {e.elapsed:.1f}s, gave up after {e.seconds}s")
```

### `@timeout_decorator` — decorate a function

```python
from agent_timeout import timeout_decorator, TimeoutExceeded

@timeout_decorator(30)
def call_llm(messages):
    return client.chat.completions.create(model="gpt-4o", messages=messages)

try:
    result = call_llm(messages)
except TimeoutExceeded:
    print("LLM call timed out")
```

### `timeout()` context manager

```python
from agent_timeout import timeout, TimeoutExceeded

# Hard enforcement via .run():
with timeout(30) as t:
    result = t.run(call_llm, messages)

# Soft enforcement — raises on exit if block was too slow:
with timeout(30):
    result = call_llm(messages)
```

### Async support

```python
from agent_timeout import with_timeout_async, timeout_async, TimeoutExceeded

# One-shot:
result = await with_timeout_async(30, client.messages.create(**params))

# Decorator:
@timeout_async(30)
async def call_llm_async(messages):
    return await async_client.messages.create(messages=messages)
```

### `TimeBudget` — cap total retry time

The most important pattern for production agents: limit the total wall-clock time across all retry attempts.

```python
from agent_timeout import TimeBudget, with_timeout, TimeoutExceeded, BudgetExhausted

budget = TimeBudget(total_seconds=60)  # 1 minute total budget

for attempt in range(5):
    try:
        per_call = budget.timeout_for(15)  # at most 15s per call, less if budget is low
        result = with_timeout(per_call, call_llm, messages)
        break  # success
    except TimeoutExceeded:
        print(f"Attempt {attempt + 1} timed out, retrying...")
        continue
    except BudgetExhausted:
        print("Total time budget exhausted, giving up")
        raise
```

`timeout_for(per_call)` returns `min(per_call, budget.remaining())`, so the last retry never runs past the total budget.

## Why threading, not signals

`signal.alarm` is Unix-only and only works in the main thread. If your LLM calls run in a thread pool, background worker, or any context other than the main thread, signal-based timeouts silently fail or raise in the wrong thread.

This library uses `threading.Thread` + `.join(timeout)` for sync code and `asyncio.wait_for` for async. Both work everywhere Python runs.

## Pairs well with

- **agent-retry**: Use `TimeBudget` to cap total retry time alongside `agent-retry`'s exponential backoff. `budget.timeout_for(per_call)` feeds directly into `with_timeout()` for each attempt.
- **agent-budget**: Track API cost while enforcing time limits. Two orthogonal guards.

## API reference

### `TimeoutExceeded(seconds, elapsed)`
- `.seconds` — the timeout limit
- `.elapsed` — actual time elapsed

### `with_timeout(seconds, func, *args, **kwargs)`
Run a callable with a hard timeout.

### `timeout(seconds)`
Context manager. Use `.run(func, *args, **kwargs)` for hard enforcement, or use as a block wrapper for elapsed-check enforcement.

### `timeout_decorator(seconds)`
Decorator. Wraps a sync function with a hard timeout.

### `with_timeout_async(seconds, coro)`
Awaitable. Wraps an async coroutine. Raises `TimeoutExceeded`, not `asyncio.TimeoutError`.

### `timeout_async(seconds)`
Decorator for async functions.

### `TimeBudget(total_seconds)`
- `.elapsed()` — seconds since creation
- `.remaining()` — seconds left (floor 0)
- `.is_exhausted` — True when remaining() == 0
- `.check()` — raises `BudgetExhausted` if exhausted
- `.timeout_for(per_call)` — returns min(per_call, remaining()), raises if exhausted
- `.reset()` — restart the timer

### `BudgetExhausted(budget, elapsed)`
- `.budget` — total budget seconds
- `.elapsed` — actual elapsed when exhausted

## License

MIT
