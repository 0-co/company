# agent-router

Zero-dependency model routing for AI agents. Route LLM API calls to different models based on configurable rules — use cheaper models for simple tasks, expensive models for complex ones.

Every production AI team does this with if/else chains buried in application code. This library makes it clean, declarative, and testable.

## When you need this

- You're calling expensive models for simple queries that a cheap model handles fine
- Your routing logic is scattered across the codebase as ad-hoc if/else checks
- You want to add routing rules without touching call sites
- You're hitting rate limits on a single model and want to spread load
- You need to log which model handled which request for cost attribution

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-router
```

Zero dependencies. Python 3.9+.

## Quick example

```python
from anthropic import Anthropic
from agent_router import Router, Route
from agent_router.rules import input_tokens_under, contains_keyword, always

client = Anthropic()

router = Router([
    # Keyword-triggered: always use the powerful model for code
    Route(
        "claude-sonnet-4-6",
        conditions=[contains_keyword("code", "function", "debug", "error")],
        max_tokens=4096,
        name="code",
    ),
    # Short input: cheap and fast
    Route(
        "claude-haiku-4-5-20251001",
        conditions=[input_tokens_under(500)],
        max_tokens=512,
        name="quick",
    ),
    # Default: everything else
    Route(
        "claude-sonnet-4-6",
        max_tokens=2048,
        name="default",
    ),
])

messages = [{"role": "user", "content": "What is the capital of France?"}]
result = router.complete(client, messages, system="You are a helpful assistant.")

print(result.route_name)   # "quick" — short input, routed to haiku
print(result.model)        # "claude-haiku-4-5-20251001"
print(result.text())       # "Paris."
```

## Cost implications

Routing correctly matters. As of early 2026:

| Model | Input cost | Output cost |
|---|---|---|
| claude-haiku-4-5-20251001 | $0.80/M tokens | $4.00/M tokens |
| claude-sonnet-4-6 | $3.00/M tokens | $15.00/M tokens |
| claude-opus-4-6 | $15.00/M tokens | $75.00/M tokens |

Haiku is ~4x cheaper than Sonnet, ~20x cheaper than Opus. If 60% of your traffic is simple queries, routing those to haiku pays for this library in the first hour.

Pair with [agent-budget](../agent-budget/) to enforce hard cost caps per session.

## Built-in routing conditions

All conditions are factory functions that return `(messages, **context) -> bool` callables.

### Token-based

```python
from agent_router.rules import input_tokens_under, input_tokens_over

# Estimated from character count (total_chars / 4) — no tokenizer needed
input_tokens_under(500)   # < 500 estimated tokens
input_tokens_over(2000)   # >= 2000 estimated tokens
```

### Message length

```python
from agent_router.rules import last_message_under, last_message_over

last_message_under(200)   # last message < 200 chars
last_message_over(1000)   # last message > 1000 chars
```

### Conversation depth

```python
from agent_router.rules import message_count_under, message_count_over

message_count_under(3)    # fewer than 3 messages (new conversation)
message_count_over(10)    # 10+ messages (deep conversation)
```

### Keyword detection

```python
from agent_router.rules import contains_keyword

# Case-insensitive by default
contains_keyword("urgent", "critical")       # any keyword matches
contains_keyword("EXACT", case_sensitive=True)
```

### Always / default

```python
from agent_router.rules import always

# Use as the last route — acts as the catch-all default
Route("claude-sonnet-4-6", conditions=[always()], ...)
# Or just omit conditions entirely — empty conditions = always matches
Route("claude-sonnet-4-6")
```

## Custom conditions

Any `(messages, **context) -> bool` function works:

```python
from agent_router.rules import custom

def is_sensitive_topic(messages, **context):
    text = ' '.join(m.get('content', '') for m in messages)
    sensitive = ['medical', 'legal', 'financial']
    return any(word in text.lower() for word in sensitive)

router = Router([
    Route("claude-opus-4-6",
          conditions=[custom(is_sensitive_topic)],
          max_tokens=4096,
          name="sensitive"),
    Route("claude-haiku-4-5-20251001", max_tokens=512, name="default"),
])
```

Context kwargs from `router.complete(..., **context)` are passed through to all conditions:

```python
def premium_user(messages, **context):
    return context.get('user_tier') == 'premium'

result = router.complete(client, messages, user_tier='premium')
```

## RouterResult

```python
result = router.complete(client, messages)

result.model       # str: model that was called
result.route_name  # str: route.name if set, else route.model
result.route       # Route: the Route object that matched
result.response    # raw response from the client (Anthropic or OpenAI)
result.text()      # str: extracted text content, works for both client types
```

## Async

```python
result = await router.acomplete(client, messages, system="...")
```

Works with both Anthropic and OpenAI async clients.

## OpenAI

Works identically with OpenAI clients:

```python
from openai import OpenAI

client = OpenAI()
router = Router([
    Route("gpt-4o-mini", conditions=[input_tokens_under(500)], max_tokens=512, name="quick"),
    Route("gpt-4o", max_tokens=4096, name="default"),
])
result = router.complete(client, messages)
```

Client detection is automatic: Anthropic clients have `.messages`, OpenAI clients have `.chat`.

## Integration

- [agent-budget](../agent-budget/) — enforce hard cost caps; combine with routing to stay within budget
- [agent-retry](../agent-retry/) — exponential backoff when routed models are overloaded
- [agent-log](../agent-log/) — log `result.route_name` and `result.model` for cost attribution

## License

MIT
