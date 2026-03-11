#!/usr/bin/env python3
"""
Agentic loop with budget enforcement.
Switches to cheaper model when cost threshold is hit.
"""
import anthropic
from agent_budget import BudgetEnforcer, BudgetExceeded

# Hard limit at $1.00, warn at 60% so we can downgrade model
enforcer = BudgetEnforcer(max_cost_usd=1.00, warn_at=0.6)
client = enforcer.wrap(anthropic.Anthropic())

def agent_step(messages, model="claude-sonnet-4-6"):
    """One step of the agent loop."""
    response = client.messages.create(
        model=model,
        max_tokens=512,
        messages=messages
    )
    return response.content[0].text

# Simple task: multi-turn conversation
messages = [{"role": "user", "content": "Plan a 5-step process to build a web scraper."}]
model = "claude-sonnet-4-6"
fallback_model = "claude-haiku-4-5-20251001"

try:
    for step in range(5):
        # Switch to cheaper model if approaching budget
        if enforcer.remaining_cost_usd is not None and enforcer.remaining_cost_usd < 0.40:
            model = fallback_model
            print(f"Budget at ${enforcer.used_cost_usd:.3f}/{enforcer.max_cost_usd}, switching to {model}")

        result = agent_step(messages, model=model)
        messages.append({"role": "assistant", "content": result})
        messages.append({"role": "user", "content": f"Continue to step {step+2}."})
        print(f"Step {step+1} done. {enforcer.status()}")

except BudgetExceeded as e:
    print(f"Agent stopped: {e}")
