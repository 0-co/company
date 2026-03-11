# agent-cache

Zero-dep LLM response caching for AI agents. Wrap your Anthropic or OpenAI client, get transparent caching, and know exactly how much money you saved.

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-cache
```

## When you need this

Your agent calls `client.messages.create()` with the same prompt 10 times during a test run. That's 9 wasted API calls — and wasted money. `agent-cache` intercepts those calls and returns the stored response from disk.

- **Costs money**: repeated prompts in evaluation loops, test suites, multi-agent systems where the same question gets asked by different agents
- **Costs time**: every API call adds latency. Cache hits are instant.
- **Costs tokens**: you're charged for the same tokens over and over

## Usage

```python
import anthropic
from agent_cache import ResponseCache

cache = ResponseCache()  # stores in ~/.cache/agent-cache/cache.json
client = cache.wrap(anthropic.Anthropic())

# First call hits the API
response = client.messages.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    max_tokens=64,
)

# Identical call — served from cache, zero API cost
response = client.messages.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    max_tokens=64,
)

# How much did we save?
print(cache.stats())
# CacheStats(hits=1, misses=1, hit_rate=50.0%, cost_saved=$0.0001)
```

Works the same way with OpenAI:

```python
import openai
from agent_cache import ResponseCache

client = ResponseCache().wrap(openai.OpenAI())
response = client.chat.completions.create(model="gpt-4o-mini", messages=[...])
```

## Options

```python
cache = ResponseCache(
    path="./my_cache.json",   # custom cache file (default: ~/.cache/agent-cache/cache.json)
    ttl=3600,                 # expire entries after N seconds (default: None = forever)
    max_entries=10_000,       # max cached responses, oldest evicted first (default: 10_000)
)
```

## What gets cached

The cache key is a SHA-256 hash of: `model`, `messages`, and any params that affect the response (`temperature`, `max_tokens`, `top_p`, `top_k`, `stop_sequences`, `system`, `seed`, etc.).

Non-deterministic params like `metadata`, `user`, `timeout` are ignored — same prompt with different metadata still hits the cache.

**Streaming calls are never cached** (OpenAI `stream=True`). They bypass the cache transparently.

## Manual API

```python
# Make a key for any request
key = cache.make_key("claude-sonnet-4-6", messages, temperature=0.0)

# Check cache
cached = cache.get(key)     # returns namespace object or None

# Store a response
cache.set(key, response, model="claude-sonnet-4-6")

# Stats
stats = cache.stats()
print(stats.hits, stats.misses, stats.hit_rate, stats.cost_saved_usd)

# Invalidate one entry
cache.invalidate(key)

# Clear everything
cache.clear()
```

## Cached response access

Cache hits return a `SimpleNamespace` with the same attribute structure as the real response:

```python
# Anthropic
response.content[0].text
response.usage.input_tokens
response.model

# OpenAI
response.choices[0].message.content
response.usage.prompt_tokens
```

## Cost tracking

Prices are hardcoded for 12 models (same table as [agent-budget](../agent-budget)):

| Model | Input | Output |
|---|---|---|
| claude-opus-4-6 | $15/M | $75/M |
| claude-sonnet-4-6 | $3/M | $15/M |
| claude-haiku-4-5 | $0.80/M | $4/M |
| gpt-4o | $2.50/M | $10/M |
| gpt-4o-mini | $0.15/M | $0.60/M |

Unknown models report $0 saved (cache still works).

## Pairs well with

- **[agent-budget](../agent-budget)** — set a hard cost ceiling; cache reduces spend toward it
- **[agent-eval](../agent-eval)** — run evals without API cost on repeated prompts
- **[agent-retry](../agent-retry)** — retries on transient errors; cache avoids re-running successful calls

## Zero dependencies

Pure Python stdlib. No Redis, no `diskcache`, no embedding models. Cache is a single JSON file.

## License

MIT
