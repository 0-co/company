"""
agent-cache example: OpenAI client with response caching.

Drop-in replacement — just wrap the client. Streaming calls bypass cache automatically.
"""

import openai
from agent_cache import ResponseCache

cache = ResponseCache(path="/tmp/openai_demo_cache.json")
client = cache.wrap(openai.OpenAI())

messages = [{"role": "user", "content": "Name a planet in our solar system."}]

for i in range(3):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=32,
    )
    print(f"Call {i+1}: {response.choices[0].message.content}")

stats = cache.stats()
print(f"\nHit rate: {stats.hit_rate:.0%}")
print(f"Cost saved: ${stats.cost_saved_usd:.6f}")
