# agent-fallback

Zero-dependency multi-provider failover for AI agents. When your primary LLM
provider returns 5xx errors or is unavailable, automatically fall back to the
next provider in the chain. The agent keeps running.

```
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-fallback
```

---

## When you need this

Anthropic 529s happen. OpenAI has outages. When you're running an agent loop
at 03:00 UTC and your provider goes down, you don't want a page — you want
the agent to seamlessly switch to the backup and keep going.

agent-retry handles transient blips on a single provider (rate limits,
momentary 503s). agent-fallback handles the case where the provider itself
is down and you need a different one.

Real scenarios:

- Anthropic returns 529 (overloaded) on the 3rd retry. Fall back to OpenAI gpt-4o.
- OpenAI is having an incident. Fall back to Anthropic.
- You want GPT-4o by default but Claude as backup for cost reasons.
- A network error (DNS, TCP reset) makes the primary unreachable.

---

## Quick start

```python
import anthropic
import openai
from agent_fallback import Fallback, Provider

fb = Fallback([
    Provider(anthropic.Anthropic(), "claude-sonnet-4-6", name="anthropic"),
    Provider(openai.OpenAI(),       "gpt-4o",            name="openai"),   # fallback
])

result = fb.complete(
    messages=[{"role": "user", "content": "What is 2+2?"}],
    system="You are a helpful assistant.",
)
print(f"Answered by: {result.provider_name}")
print(result.text())
```

Three-provider chain:

```python
fb = Fallback([
    Provider(anthropic.Anthropic(), "claude-sonnet-4-6", name="primary"),
    Provider(openai.OpenAI(),       "gpt-4o",            name="backup-1"),
    Provider(openai.OpenAI(),       "gpt-3.5-turbo",     name="backup-2"),
])
result = fb.complete(messages)
```

---

## Retryable vs non-retryable errors

agent-fallback distinguishes between "provider is broken" and "your request
is broken":

| Status code | Retryable | Reason |
|-------------|-----------|--------|
| 500         | Yes       | Provider error, try another |
| 502         | Yes       | Bad gateway |
| 503         | Yes       | Service unavailable |
| 529         | Yes       | Anthropic overloaded |
| ConnectionError / TimeoutError / OSError | Yes | Network issue |
| 400         | No        | Bad request — won't fix itself |
| 401         | No        | Auth error — won't fix itself |
| 403         | No        | Forbidden |
| 429         | No        | Rate-limited — provider IS up, just throttling |

429 is intentionally non-retryable. If you're rate-limited, switching to
another provider won't help you stay under your primary provider's limits,
and it's a sign the provider is running fine — you're just over quota.

---

## on_fallback callback

Log when a fallback happens:

```python
def on_fallback(provider, error):
    print(f"Provider {provider.name} failed: {error}. Trying next...")

fb = Fallback(providers, on_fallback=on_fallback)
```

---

## Async support

```python
result = await fb.acomplete(
    messages=[{"role": "user", "content": "hi"}],
    system="Be helpful.",
)
```

---

## CircuitBreaker

Stop hammering a dead provider. The circuit breaker tracks failures per
provider and skips it during cooldown:

```python
from agent_fallback import CircuitBreaker, CircuitOpen

breaker = CircuitBreaker(failure_threshold=3, cooldown_seconds=60)

try:
    with breaker:
        result = call_api()
except CircuitOpen as exc:
    print(f"Circuit open. {exc.cooldown_remaining:.0f}s until reset.")
```

Using a circuit breaker with Fallback:

```python
breakers = {
    "anthropic": CircuitBreaker(failure_threshold=3, cooldown_seconds=60, name="anthropic"),
    "openai":    CircuitBreaker(failure_threshold=3, cooldown_seconds=60, name="openai"),
}

def call_with_breaker(provider_name, call_fn):
    breaker = breakers[provider_name]
    try:
        with breaker:
            return call_fn()
    except CircuitOpen:
        raise ConnectionError(f"{provider_name} circuit open")

# Wire into on_fallback
def on_fallback(provider, error):
    print(f"{provider.name} failed, circuit recorded")
```

The circuit auto-resets to closed after `cooldown_seconds` without requiring
any action — a clean retry will succeed if the provider recovered.

---

## Reliability trilogy

| Library | Handles |
|---------|---------|
| [agent-retry](../agent-retry/) | Transient errors on the same provider (backoff + jitter) |
| [agent-timeout](../agent-timeout/) | Deadline enforcement — kill a call that takes too long |
| **agent-fallback** | Provider-level failover — when the provider itself is down |

They compose: use agent-retry inside each provider's call, agent-timeout as
the outer deadline, and agent-fallback to route between providers.

---

## API reference

### `Provider`

```python
@dataclass
class Provider:
    client: Any          # Anthropic or OpenAI client
    model: str           # model name
    name: str = ""       # friendly name (defaults to model name)
    max_tokens: int = 1024
```

### `Fallback`

```python
class Fallback:
    def __init__(
        self,
        providers: list[Provider],
        retryable_status_codes: set[int] = None,  # default: {500, 502, 503, 529}
        on_fallback: Callable = None,              # callback(provider, error)
    )

    def complete(
        self,
        messages: list,
        system: str = None,
        extra_params: dict = None,
    ) -> FallbackResult

    async def acomplete(...) -> FallbackResult
```

### `FallbackResult`

```python
result.response        # raw SDK response object
result.provider        # Provider instance that succeeded
result.provider_name   # str — same as result.provider.name
result.attempt         # int — 1-indexed (1 = primary succeeded)
result.text()          # str — extracted text (Anthropic + OpenAI formats)
```

### `ProviderFailed`

Raised when all providers have been exhausted.

```python
try:
    result = fb.complete(messages)
except ProviderFailed as exc:
    for provider_name, error in exc.errors:
        print(f"{provider_name}: {error}")
```

### `CircuitBreaker`

```python
class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        cooldown_seconds: float = 60.0,
        name: str = "",
    )

    is_open: bool              # True if provider in cooldown
    cooldown_remaining: float  # seconds until auto-reset

    def record_failure()
    def record_success()
    def reset()                # force back to closed

    # Context manager: raises CircuitOpen if open
    # Records failure/success automatically on exit
    with breaker: ...
```

---

## Zero dependencies

stdlib only: `threading`, `asyncio`, `time`. Works with Anthropic and OpenAI
SDKs when installed, but neither is required.

MIT License.
