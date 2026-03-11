#!/usr/bin/env python3
"""Basic usage: enforce a $0.10 budget on an Anthropic client."""
import anthropic
from agent_budget import BudgetEnforcer, BudgetExceeded

enforcer = BudgetEnforcer(max_cost_usd=0.10, warn_at=0.8)
client = enforcer.wrap(anthropic.Anthropic())

try:
    for i in range(10):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[{"role": "user", "content": f"Count to {i+1}."}]
        )
        print(f"Turn {i+1}: {response.content[0].text[:50]}")
        print(f"  {enforcer.status()}")
except BudgetExceeded as e:
    print(f"Budget hit: {e}")
    print(f"  Used: {enforcer.used_cost_usd:.4f} USD")
