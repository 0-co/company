# agent-rate

Zero-dependency rate limiting for AI agent API calls.

Prevents hitting provider rate limits by smoothing call frequency.
Token bucket algorithm, supports requests-per-minute and tokens-per-minute limiting, sync and async, with decorator and context manager interfaces.

## Why this matters

The standard solution for rate limiting LLM calls is `time.sleep(1.2)` between requests. This is wrong in two ways:

1. **It burns time you don't need to.** If the last request was 0.8s ago and your rate limit is 1 req/sec, you only need to wait 0.2s — not 1.2s.
2. **It breaks under concurrency.** Multiple coroutines all sleeping the same fixed interval will fire simultaneously and immediately saturate the rate limit.

A proper token bucket gives burst allowance while maintaining the correct average rate, and works correctly whether you have one caller or twenty.

## When you need this

- You're calling an LLM API in a loop and hitting 429s
- You're running concurrent agent tasks and need to coordinate their API usage
- You want to track both request rate and token consumption simultaneously
- You're integrating with `agent-retry` and want to prevent the 429s before they trigger retries

## Installation

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-rate
```

Zero dependencies. Python 3.9+.

## Quick start

### Basic RPM limiting

```python
from agent_rate import RateLimiter

limiter = RateLimiter(requests_per_minute=50)

# Blocking — waits if needed, returns seconds waited
limiter.limit()
result = client.messages.create(model="claude-opus-4-6", ...)
```

### RPM + TPM

```python
limiter = RateLimiter(
    requests_per_minute=50,
    tokens_per_minute=100_000,
)

# Pass estimated token count before each call
limiter.limit(token_count=1_500)
result = client.messages.create(...)
```

### Non-blocking (raise instead of wait)

```python
from agent_rate import RateLimiter, RateLimitExceeded

limiter = RateLimiter(requests_per_minute=50)

try:
    limiter.limit(block=False)
    result = client.messages.create(...)
except RateLimitExceeded as e:
    print(f"Rate limited. Retry in {e.retry_after:.2f}s")
```

### Decorator

```python
limiter = RateLimiter(requests_per_minute=50)

@limiter.rate_limited
def call_llm(messages):
    return client.messages.create(model="claude-opus-4-6", messages=messages)

# limit() is called automatically before each invocation
response = call_llm([{"role": "user", "content": "hello"}])
```

### Context manager

```python
with limiter:
    result = client.messages.create(...)
```

### Async

```python
limiter = RateLimiter(requests_per_minute=50)

# Async limit
await limiter.alimit()
result = await async_client.messages.create(...)

# Async decorator
@limiter.rate_limited_async
async def call_llm(prompt):
    return await async_client.messages.create(...)
```

## Token bucket vs sliding window

Two algorithms are available.

### Token bucket (recommended)

```python
from agent_rate import RateLimiter

limiter = RateLimiter(requests_per_minute=60, burst_factor=1.5)
```

- Allows short bursts up to `burst_factor * rate` (default: 1.5x)
- Correctly handles idle periods — unused capacity accumulates (up to burst limit)
- Better for API calls where occasional bursts are fine

### Sliding window counter

```python
from agent_rate import SlidingWindowLimiter

limiter = SlidingWindowLimiter(max_requests=60, window_seconds=60)
```

- Strict: exactly `max_requests` in any `window_seconds` period
- No burst allowance
- Slightly more predictable if you need strict compliance

## Burst factor

The token bucket starts full and refills at `requests_per_minute / 60` tokens per second.
Capacity is `burst_factor * requests_per_minute / 60`. Default burst_factor is 1.5.

At 60 RPM with burst_factor=1.5: capacity is 1.5 tokens. After an idle period you can
fire 1 request immediately plus one more ~0.67s later — rather than waiting a full second
for the first slot.

## Integration with agent-retry

```python
from agent_rate import RateLimiter
from agent_retry import retry_with_backoff

limiter = RateLimiter(requests_per_minute=50)

@retry_with_backoff(max_retries=3)
def call_llm(messages):
    limiter.limit()  # prevents the 429s that would trigger retries
    return client.messages.create(model="claude-opus-4-6", messages=messages)
```

## API reference

### RateLimiter

| Parameter | Default | Description |
|---|---|---|
| `requests_per_minute` | `60` | Request rate limit |
| `tokens_per_minute` | `None` | Token rate limit (None = no token limiting) |
| `burst_factor` | `1.5` | Burst capacity multiplier |

| Method | Description |
|---|---|
| `limit(token_count=0, block=True)` | Acquire permission. Returns seconds waited. |
| `alimit(token_count=0, block=True)` | Async version. |
| `rate_limited(func)` | Decorator — calls `limit()` before each call. |
| `rate_limited_async(func)` | Async decorator. |
| `reset()` | Fill both buckets to capacity. |

| Property | Description |
|---|---|
| `requests_available` | Current request bucket level. |
| `tokens_available` | Current token bucket level. `None` if TPM not configured. |

### SlidingWindowLimiter

| Parameter | Default | Description |
|---|---|---|
| `max_requests` | required | Max requests in window |
| `window_seconds` | `60` | Window duration in seconds |

| Method | Description |
|---|---|
| `limit(block=True)` | Acquire permission. Returns seconds waited. |
| `alimit(block=True)` | Async version. |

| Property | Description |
|---|---|
| `current_count` | Requests in current window. |
| `remaining` | Requests remaining before window fills. |

### RateLimitExceeded

Raised when `block=False` and the rate limit is exceeded.

| Attribute | Type | Description |
|---|---|---|
| `retry_after` | `float` | Seconds until next slot is available. |

## License

MIT
