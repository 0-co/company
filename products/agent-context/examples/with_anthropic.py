#!/usr/bin/env python3
"""with_anthropic.py — agent loop using ContextManager with the Anthropic SDK.

This shows the pattern for real multi-turn agents. Without context management,
every turn sends the full history. After ~30 turns, quality starts degrading
and costs compound. ContextManager fixes both.

Requirements:
    pip install anthropic
    export ANTHROPIC_API_KEY=your-key-here
"""

import os
import sys

try:
    import anthropic
except ImportError:
    print("anthropic SDK not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)

from agent_context import ContextManager, ContextOverflow

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not API_KEY:
    print("Set ANTHROPIC_API_KEY environment variable.", file=sys.stderr)
    sys.exit(1)

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS_RESPONSE = 256

# Keep a rolling 10-turn window. For long-running agents, adjust max_tokens
# based on the model's context limit minus your expected response size.
ctx = ContextManager(
    max_turns=10,
    system=(
        "You are a concise assistant. "
        "Answer directly and briefly. "
        "If asked something you don't know, say so."
    ),
)

client = anthropic.Anthropic(api_key=API_KEY)

# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

QUESTIONS = [
    "What is the capital of France?",
    "What river runs through it?",
    "Name one famous bridge over that river.",
    "How old is that bridge approximately?",
    "What materials was it built from?",
    "Is it still used today?",
    "How many people visit Paris each year roughly?",
    "What is the most visited monument there?",
    "How tall is it?",
    "When was it built?",
    "Who designed it?",
    "What was the original purpose?",
]


def run_agent_loop() -> None:
    """Run a multi-turn conversation and print window stats each turn."""
    print(f"Model: {MODEL}")
    print(f"Strategy: sliding_window, max_turns=10")
    print(f"Questions: {len(QUESTIONS)}")
    print("-" * 60)

    for turn, question in enumerate(QUESTIONS, start=1):
        ctx.add("user", question)

        # ctx.get() returns the trimmed window — system message prepended.
        messages = ctx.get()
        # Anthropic API takes system separately, not as a message role.
        system_text = None
        non_system = []
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            else:
                non_system.append(msg)

        kwargs = dict(
            model=MODEL,
            max_tokens=MAX_TOKENS_RESPONSE,
            messages=non_system,
        )
        if system_text:
            kwargs["system"] = system_text

        response = client.messages.create(**kwargs)
        answer = response.content[0].text.strip()

        ctx.add("assistant", answer)

        print(
            f"Turn {turn:2d} | window={ctx.current_turns:2d} msgs"
            f" | ~{ctx.tokens_estimate:4d} tokens"
            f" | Q: {question[:40]}"
        )
        print(f"         A: {answer[:80]}")

    print("-" * 60)
    print(f"Total turns added: {ctx.total_turns}")
    print(f"Final window size: {ctx.current_turns} messages")
    print(f"Final token estimate: {ctx.tokens_estimate}")


# ---------------------------------------------------------------------------
# Alternative: token budget strategy
# ---------------------------------------------------------------------------

def run_with_token_budget() -> None:
    """Same loop but using token budget instead of turn count.

    Useful when messages vary wildly in length — a 10-turn window might be
    8,000 tokens with verbose answers or 400 with terse ones. Token budget
    gives tighter control.
    """
    ctx_tokens = ContextManager(
        max_tokens=2000,
        system="You are a concise assistant.",
    )
    # This would follow the same loop structure as above but pass ctx_tokens
    # instead of ctx. Not run here to avoid duplicate API calls.
    print("Token budget ContextManager configured (not run in this example).")
    print(f"  strategy: {ctx_tokens._effective_strategy}")
    print(f"  max_tokens: {ctx_tokens._max_tokens}")


# ---------------------------------------------------------------------------
# Alternative: compress strategy with real summarizer
# ---------------------------------------------------------------------------

def make_summarizer(api_client: "anthropic.Anthropic") -> callable:
    """Return a summarizer that uses Claude to compress middle turns.

    The returned function is passed to ContextManager(summarizer=...).
    It condenses dropped messages into a single summary message so the
    model retains high-level context without the full token cost.
    """
    def summarize(messages: list[dict]) -> str:
        """Call Claude to summarize a slice of conversation history."""
        combined = "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in messages
        )
        prompt = (
            f"Summarize the following conversation excerpt in 2-3 sentences. "
            f"Keep only the key facts and decisions:\n\n{combined}"
        )
        response = api_client.messages.create(
            model=MODEL,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()

    return summarize


def show_compress_setup() -> None:
    """Print how to set up the compress strategy (not run to avoid API calls)."""
    print("\nCompress strategy setup (not run in this example):")
    print(
        "  summarizer = make_summarizer(client)\n"
        "  ctx = ContextManager(\n"
        "      max_turns=20,\n"
        "      strategy='compress',\n"
        "      summarizer=summarizer,\n"
        "      keep_first=2,\n"
        "      keep_last=4,\n"
        "  )"
    )


if __name__ == "__main__":
    run_agent_loop()
    run_with_token_budget()
    show_compress_setup()
