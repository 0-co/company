#!/usr/bin/env python3
"""basic_usage.py — demonstrate all scorer types with a mock agent.

No LLM calls. The mock agent returns predictable strings so every
test outcome is deterministic.

Run:
    python examples/basic_usage.py
"""

from agent_eval import Case, Eval, EvalFailed, EvalResults, RunResult, run


# ---------------------------------------------------------------------------
# Mock agent: returns predictable answers for known inputs
# ---------------------------------------------------------------------------

ANSWERS = {
    "What is 2+2?": "4",
    "Capital of France?": "The capital city is Paris.",
    "Is water wet?": "Yes, water is wet.",
    "Summarize in one word": "Done.",
    "Cause an error": None,          # trigger KeyError on purpose
    "Slow call": "eventually done",  # used for timeout demo
}


def mock_agent(input_text: str) -> str:
    """Return a canned answer or raise if answer is None."""
    answer = ANSWERS.get(input_text)
    if answer is None:
        raise RuntimeError(f"mock_agent: no answer for input: {input_text!r}")
    return answer


# ---------------------------------------------------------------------------
# Demonstrate: exact scorer
# ---------------------------------------------------------------------------

def demo_exact() -> None:
    """exact: output.strip() == expected.strip() (case-sensitive)."""
    print("=== exact scorer ===")
    results = run(
        mock_agent,
        [
            Case("What is 2+2?", expected="4", scorer="exact", label="basic arithmetic"),
            # This one will fail: agent returns "The capital city is Paris."
            Case("Capital of France?", expected="Paris", scorer="exact", label="exact city (fails)"),
        ],
    )
    print(results.summary())
    print()


# ---------------------------------------------------------------------------
# Demonstrate: contains scorer
# ---------------------------------------------------------------------------

def demo_contains() -> None:
    """contains: expected.lower() in output.lower() — partial match, case-insensitive."""
    print("=== contains scorer ===")
    results = run(
        mock_agent,
        [
            Case("Capital of France?", expected="Paris", scorer="contains", label="capital city"),
            Case("Is water wet?", expected="wet", scorer="contains", label="wetness check"),
        ],
    )
    print(results.summary())
    print()


# ---------------------------------------------------------------------------
# Demonstrate: regex scorer
# ---------------------------------------------------------------------------

def demo_regex() -> None:
    """regex: re.search(expected, output, IGNORECASE) — pattern match."""
    print("=== regex scorer ===")
    results = run(
        mock_agent,
        [
            Case("Is water wet?", expected=r"yes|wet", scorer="regex", label="yes or wet"),
            Case("What is 2+2?", expected=r"^\d+$", scorer="regex", label="digit-only answer"),
        ],
    )
    print(results.summary())
    print()


# ---------------------------------------------------------------------------
# Demonstrate: None scorer (baseline — always passes)
# ---------------------------------------------------------------------------

def demo_none_scorer() -> None:
    """scorer=None: always passes. Useful as a smoke test baseline."""
    print("=== None scorer (always passes) ===")
    results = run(
        mock_agent,
        [
            Case("Summarize in one word", scorer=None, label="any output is fine"),
        ],
    )
    print(results.summary())
    print()


# ---------------------------------------------------------------------------
# Demonstrate: custom scorer (callable)
# ---------------------------------------------------------------------------

def demo_custom_scorer() -> None:
    """Custom scorer: any callable (input, output, expected) -> bool | float."""
    print("=== custom scorer ===")

    def concise_check(inp: str, out: str, exp: str | None) -> bool:
        """Pass if the output is under 20 characters."""
        return len(out) < 20

    def contains_and_concise(inp: str, out: str, exp: str | None) -> bool:
        """Pass if output contains expected and is under 100 chars."""
        return (exp is not None and exp.lower() in out.lower()) and len(out) < 100

    results = run(
        mock_agent,
        [
            Case("What is 2+2?", scorer=concise_check, label="answer must be concise"),
            # "The capital city is Paris." is 26 chars, so concise_check will fail.
            Case(
                "Capital of France?",
                scorer=concise_check,
                label="city answer too long (fails)",
            ),
            Case(
                "Is water wet?",
                expected="wet",
                scorer=contains_and_concise,
                label="contains wet + under 100 chars",
            ),
            # Lambda: inline one-liner
            Case(
                "Summarize in one word",
                scorer=lambda i, o, e: len(o.split()) == 1,
                label="exactly one word",
            ),
        ],
    )
    print(results.summary())
    print()


# ---------------------------------------------------------------------------
# Demonstrate: agent raises exception
# ---------------------------------------------------------------------------

def demo_agent_error() -> None:
    """When agent_fn raises, the run fails with passed=False and error set."""
    print("=== agent raises exception ===")
    results = run(
        mock_agent,
        [
            Case("Cause an error", scorer=None, label="agent raises RuntimeError"),
            Case("What is 2+2?", expected="4", scorer="exact", label="normal case still runs"),
        ],
    )
    print(results.summary())
    for r in results:
        if r.error:
            print(f"  error detail: {r.error}")
    print()


# ---------------------------------------------------------------------------
# Demonstrate: Eval class (stateful, accumulates cases)
# ---------------------------------------------------------------------------

def demo_eval_class() -> None:
    """Eval accumulates cases and runs them all at once."""
    print("=== Eval class ===")

    e = Eval()
    e.add(Case("What is 2+2?", expected="4", scorer="exact"))
    e.add(Case("Capital of France?", expected="Paris", scorer="contains"))
    e.add(Case("Is water wet?", expected=r"yes|wet", scorer="regex"))
    e.add(Case("Summarize in one word", scorer=None))

    results = e.run(mock_agent)
    print(results.summary())
    print(f"score property: {results.score:.2f}")
    print(f"passed/total: {results.passed}/{results.total}")
    print()


# ---------------------------------------------------------------------------
# Demonstrate: assert_all_passed for CI
# ---------------------------------------------------------------------------

def demo_assert() -> None:
    """assert_all_passed raises EvalFailed if any case failed."""
    print("=== assert_all_passed (CI integration) ===")

    e = Eval()
    e.add(Case("What is 2+2?", expected="4", scorer="exact"))
    e.add(Case("Capital of France?", expected="Paris", scorer="exact"))  # will fail

    results = e.run(mock_agent)
    try:
        results.assert_all_passed()
        print("All passed (this line would not print if any failed)")
    except EvalFailed as exc:
        print(f"EvalFailed raised: {exc}")
    print()


# ---------------------------------------------------------------------------
# Demonstrate: iterate over RunResult
# ---------------------------------------------------------------------------

def demo_iterate() -> None:
    """Each RunResult carries case, output, passed, score, error, duration_ms."""
    print("=== iterate RunResult ===")
    results = run(
        mock_agent,
        [
            Case("What is 2+2?", expected="4", scorer="exact"),
            Case("Capital of France?", expected="Paris", scorer="contains"),
        ],
    )
    for r in results:
        print(
            f"  input={r.case.input!r} "
            f"output={r.output!r} "
            f"passed={r.passed} "
            f"score={r.score:.1f} "
            f"duration={r.duration_ms:.1f}ms"
        )
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo_exact()
    demo_contains()
    demo_regex()
    demo_none_scorer()
    demo_custom_scorer()
    demo_agent_error()
    demo_eval_class()
    demo_assert()
    demo_iterate()
