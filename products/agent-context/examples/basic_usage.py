#!/usr/bin/env python3
"""basic_usage.py — demonstrates all three strategies with no LLM calls."""

from agent_context import ContextManager, ContextOverflow, trim

# ---------------------------------------------------------------------------
# 1. Sliding window — keep last N messages
# ---------------------------------------------------------------------------

print("=== Sliding window (max_turns=4) ===")
ctx = ContextManager(max_turns=4, system="You are a helpful assistant.")

for i in range(8):
    ctx.add("user", f"Question {i+1}: what is {i+1} + {i+1}?")
    ctx.add("assistant", f"That is {(i+1)*2}.")

messages = ctx.get()
print(f"Total turns added:    {ctx.total_turns}")
print(f"Turns in window:      {ctx.current_turns}")
print(f"Messages in get():    {len(messages)}")
print(f"First message role:   {messages[0]['role']}")   # system
print(f"Last user question:   {messages[-2]['content']}")
print()

# ---------------------------------------------------------------------------
# 2. Token budget — keep newest messages that fit
# ---------------------------------------------------------------------------

print("=== Token budget (max_tokens=100) ===")
ctx2 = ContextManager(max_tokens=100)

ctx2.add("user", "Tell me about the French Revolution.")
ctx2.add("assistant", "The French Revolution began in 1789 and fundamentally changed France.")
ctx2.add("user", "Who was Louis XVI?")
ctx2.add("assistant", "Louis XVI was king of France, executed in 1793.")
ctx2.add("user", "What happened after?")
ctx2.add("assistant", "Napoleon rose to power in 1799.")

messages2 = ctx2.get()
print(f"Total turns added:    {ctx2.total_turns}")
print(f"Token estimate:       {ctx2.tokens_estimate}")
print(f"Messages in window:   {len(messages2)}")
print()

# ---------------------------------------------------------------------------
# 3. Compress strategy — summarize the middle
# ---------------------------------------------------------------------------

print("=== Compress strategy (keep_first=2, keep_last=2) ===")

def simple_summarizer(messages: list[dict]) -> str:
    """Dummy summarizer: return a count + first snippet."""
    count = len(messages)
    snippet = messages[0]["content"][:40] if messages else ""
    return f"[{count} messages omitted. First: '{snippet}...']"

ctx3 = ContextManager(
    max_turns=10,
    strategy="compress",
    summarizer=simple_summarizer,
    keep_first=2,
    keep_last=2,
)

for i in range(10):
    ctx3.add("user", f"Step {i+1}: process item {i+1}.")
    ctx3.add("assistant", f"Item {i+1} processed successfully.")

messages3 = ctx3.get()
print(f"Total turns added:    {ctx3.total_turns}")
print(f"Messages in window:   {len(messages3)}")
for msg in messages3:
    print(f"  [{msg['role']:9s}] {msg['content'][:70]}")
print()

# ---------------------------------------------------------------------------
# 4. raise_on_overflow
# ---------------------------------------------------------------------------

print("=== raise_on_overflow ===")
ctx4 = ContextManager(max_turns=3, raise_on_overflow=True)

try:
    for i in range(5):
        ctx4.add("user", f"message {i+1}")
except ContextOverflow as exc:
    print(f"Caught: {exc}")
print()

# ---------------------------------------------------------------------------
# 5. Functional trim() interface
# ---------------------------------------------------------------------------

print("=== trim() functional interface ===")
history = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"},
    {"role": "assistant", "content": "Doing well, thanks."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
]

short = trim(history, max_turns=2, system="You are helpful.")
print(f"After trim(max_turns=2): {len(short)} messages")
for msg in short:
    print(f"  [{msg['role']:9s}] {msg['content']}")
