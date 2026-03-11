# agent-budget

AI agents blow API budgets. There's no simple way to stop this. agent-budget is a one-line fix.

---

## Install

```bash
pip install agent-budget
```

Or directly from source:

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-budget
```

---

## Quick start

```python
import anthropic
from agent_budget import BudgetEnforcer, BudgetExceeded

enforcer = BudgetEnforcer(max_cost_usd=2.50, warn_at=0.8)
client = enforcer.wrap(anthropic.Anthropic())

try:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": "hello"}]
    )
    print(response.content[0].text)
    print(enforcer.status())
    # Tokens: 1,234 / no limit (-)
    # Cost:   $0.0037 / $2.50 (0.1%)

except BudgetExceeded as e:
    print(f"Budget hit: {e}")
```

That's it. `client` behaves exactly like a normal `anthropic.Anthropic()` instance. Every call is tracked automatically.

---

## API reference

### `BudgetEnforcer(max_tokens=None, max_cost_usd=None, warn_at=0.8, model="claude-sonnet-4-6")`

At least one of `max_tokens` or `max_cost_usd` is required.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `max_tokens` | int | None | Hard stop when total tokens (input + output) reaches this value |
| `max_cost_usd` | float | None | Hard stop when total cost reaches this value (USD) |
| `warn_at` | float | 0.8 | Print a warning to stderr when usage hits this fraction of the limit |
| `model` | str | "claude-sonnet-4-6" | Default model for cost calculations when a call doesn't specify one |

#### Methods

**`track(input_tokens, output_tokens, model=None)`**

Update counters for one API call. Raises `BudgetExceeded` if a limit is crossed. You normally don't call this directly — `wrap()` handles it.

**`wrap(client)`**

Returns a proxied version of an Anthropic or OpenAI client. All attributes are forwarded transparently; only `messages.create`, `messages.stream` (Anthropic) and `chat.completions.create` (OpenAI) are intercepted for tracking.

If the client is neither Anthropic nor OpenAI, it is returned unwrapped with a warning.

**`status() -> str`**

```
Tokens: 1,234 / 50,000 (2.5%)
Cost:   $0.0185 / $2.50 (0.7%)
```

**`reset()`**

Reset all counters and warning flags. Useful for budget windows (e.g., per-request limits in a server).

#### Properties

| Property | Type | Description |
|---|---|---|
| `used_tokens` | int | Total tokens consumed so far |
| `used_cost_usd` | float | Total cost in USD so far |
| `remaining_tokens` | int or None | Tokens left before hard stop (None if no token limit) |
| `remaining_cost_usd` | float or None | USD left before hard stop (None if no cost limit) |

---

### `BudgetExceeded`

Raised when a limit is hit. Inherits from `Exception`.

```python
except BudgetExceeded as e:
    print(e.limit_type)    # "tokens" or "cost"
    print(e.limit)         # configured limit value
    print(e.used)          # value at time of violation
    print(e.model)         # model that triggered it (may be None)
    print(e.msg)           # human-readable description (also str(e))
```

---

## OpenAI example

```python
import openai
from agent_budget import BudgetEnforcer, BudgetExceeded

enforcer = BudgetEnforcer(max_cost_usd=1.00, warn_at=0.7)
client = enforcer.wrap(openai.OpenAI())

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "What is 2+2?"}]
    )
    print(response.choices[0].message.content)
    print(enforcer.status())

except BudgetExceeded as e:
    print(f"Stopped: {e}")
```

---

## Agentic loop example

Budget enforcement is most useful in loops where you don't know how many calls you'll make. This example degrades gracefully by switching to a cheaper model when approaching the limit:

```python
import anthropic
from agent_budget import BudgetEnforcer, BudgetExceeded

enforcer = BudgetEnforcer(max_cost_usd=1.00, warn_at=0.6)
client = enforcer.wrap(anthropic.Anthropic())

model = "claude-sonnet-4-6"
fallback = "claude-haiku-4-5-20251001"
messages = [{"role": "user", "content": "Plan a 5-step process to build a web scraper."}]

try:
    for step in range(5):
        # Downgrade model if more than 60% of budget is gone
        if enforcer.remaining_cost_usd is not None and enforcer.remaining_cost_usd < 0.40:
            model = fallback
            print(f"Switching to {model} (${enforcer.used_cost_usd:.3f} used)")

        response = client.messages.create(
            model=model, max_tokens=512, messages=messages
        )
        text = response.content[0].text
        messages.append({"role": "assistant", "content": text})
        messages.append({"role": "user", "content": f"Continue to step {step+2}."})
        print(f"Step {step+1}: {enforcer.status()}")

except BudgetExceeded as e:
    print(f"Agent stopped: budget exceeded ({e.limit_type})")
    print(f"Used: {enforcer.used_cost_usd:.4f} USD, {enforcer.used_tokens:,} tokens")
```

---

## Streaming

The Anthropic proxy also wraps `messages.stream`:

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
# Token usage is tracked when the context manager exits.
print(f"\n{enforcer.status()}")
```

---

## Supported models and pricing

Prices as of March 2026 (per 1M tokens):

| Model | Input | Output |
|---|---|---|
| claude-opus-4-6 | $15.00 | $75.00 |
| claude-sonnet-4-6 | $3.00 | $15.00 |
| claude-haiku-4-5-20251001 | $0.80 | $4.00 |
| claude-haiku-4-5 | $0.80 | $4.00 |
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |
| gpt-4-turbo | $10.00 | $30.00 |
| gpt-3.5-turbo | $0.50 | $1.50 |

Unknown models are tracked (token counts accumulate) but cost is not calculated — no error is raised.

---

## Why not Langfuse or Helicone?

Those are observability platforms. They require an account, a dashboard, a data pipeline, and SDK wrappers around your entire stack. They're useful when you need logging, replay, and team visibility.

agent-budget requires zero infrastructure. No account. No config file. No network call. It runs entirely in-process, raises a Python exception when you hit the limit, and gets out of the way.

If you want a bill-sized exception and nothing else, that's what this is.

---

Built at [0co](https://github.com/0-co/company) — an AI autonomously running a startup.
