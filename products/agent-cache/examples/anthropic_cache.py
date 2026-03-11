"""
agent-cache example: Anthropic client with response caching.

First call hits the API. Subsequent identical calls are served from cache.
At the end, print how much money was saved.
"""

import anthropic
from agent_cache import ResponseCache

cache = ResponseCache(
    path="/tmp/demo_cache.json",
    ttl=3600,  # cache for 1 hour
)

client = cache.wrap(anthropic.Anthropic())

# Simulate an agent that calls the same prompt multiple times
question = "What is 2 + 2?"

for i in range(3):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        messages=[{"role": "user", "content": question}],
    )
    text = response.content[0].text
    print(f"Call {i+1}: {text[:60]}")

stats = cache.stats()
print(f"\nCache stats: {stats}")
print(f"Saved: ${stats.cost_saved_usd:.6f} ({stats.hits} cache hits)")
