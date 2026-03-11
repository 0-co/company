"""
agent-mock example: fixture mode for deterministic testing.

Pre-define what the API should return. No network calls, no cost.
"""

import anthropic
from agent_mock import MockSession

session = MockSession()

# Register fixtures
session.on(
    model="claude-haiku-4-5-20251001",
    messages=[{"role": "user", "content": "Is this spam?"}],
    returns={
        "content": [{"type": "text", "text": "yes"}],
    },
)
session.on(
    model="claude-haiku-4-5-20251001",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    returns={
        "content": [{"type": "text", "text": "4"}],
    },
)

client = session.wrap(anthropic.Anthropic())

# These calls never hit the real API
r1 = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=64,
    messages=[{"role": "user", "content": "Is this spam?"}],
)
r2 = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=64,
    messages=[{"role": "user", "content": "What is 2+2?"}],
)

print(f"Spam check: {r1.content[0].text}")  # yes
print(f"Math: {r2.content[0].text}")        # 4
print(f"Total calls to API: 0")
print(f"Session call count: {session.call_count}")
