#!/usr/bin/env python3
"""with_anthropic.py — eval a real Anthropic agent with CI integration.

This script shows the recommended CI pattern:

    results = eval.run(agent)
    results.assert_all_passed()   # exits non-zero if any fail

Prerequisites:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-...

Run:
    python examples/with_anthropic.py
"""

import os
import sys

try:
    import anthropic
except ImportError:
    print("anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)

from agent_eval import Case, Eval, EvalFailed


# ---------------------------------------------------------------------------
# Build the agent function
# ---------------------------------------------------------------------------

def make_anthropic_agent(model: str = "claude-haiku-4-5-20251001") -> object:
    """Return a simple single-turn Anthropic agent callable.

    The returned function takes a str prompt and returns a str response.
    It keeps an Anthropic client alive across calls.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    def agent(prompt: str) -> str:
        """Send prompt to Anthropic, return the first text block."""
        response = client.messages.create(
            model=model,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    return agent


# ---------------------------------------------------------------------------
# Define the eval suite
# ---------------------------------------------------------------------------

def build_eval() -> Eval:
    """Construct the evaluation suite.

    These tests check that the model answers basic factual questions
    and respects simple output format constraints.
    """
    e = Eval()

    # Factual knowledge
    e.add(Case(
        "What is the capital of France? Answer in one word.",
        expected="Paris",
        scorer="contains",
        label="capital of France",
    ))
    e.add(Case(
        "What is 2 + 2? Reply with just the number.",
        expected=r"^\s*4\s*$",
        scorer="regex",
        label="basic arithmetic",
    ))
    e.add(Case(
        "Name the primary language used to write CPython.",
        expected="Python",
        scorer="contains",
        label="CPython implementation language",
    ))

    # Output format constraints (custom scorer)
    e.add(Case(
        "In one sentence, define 'API'. Be concise.",
        scorer=lambda i, o, e: len(o) < 300,
        label="API definition under 300 chars",
    ))

    # Baseline: any coherent response
    e.add(Case(
        "Say the word 'ready'.",
        expected="ready",
        scorer="contains",
        label="readiness check",
    ))

    return e


# ---------------------------------------------------------------------------
# Main: run eval, print results, assert for CI
# ---------------------------------------------------------------------------

def main() -> None:
    model = os.environ.get("EVAL_MODEL", "claude-haiku-4-5-20251001")
    print(f"Model: {model}")
    print()

    agent = make_anthropic_agent(model=model)
    e = build_eval()

    print("Running eval suite...")
    results = e.run(agent)

    print(results.summary())
    print()
    print(f"Score: {results.score * 100:.1f}%")

    # CI integration: non-zero exit if any case fails.
    # assert_all_passed() raises EvalFailed, which propagates as exit code 1.
    try:
        results.assert_all_passed()
        print("All cases passed.")
    except EvalFailed as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
