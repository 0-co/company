"""agent-eval — minimal evaluation harness for AI agents.

Define test cases with inputs and expected outputs, run them against any
agent function (str -> str), get pass/fail/score results.

Public API
----------
    Case        — a single test case with input, expected output, and scorer
    Eval        — stateful harness that accumulates cases and runs them
    EvalResults — result set returned by Eval.run()
    RunResult   — result for a single case run
    EvalFailed  — raised by EvalResults.assert_all_passed()
    run         — standalone function: run cases against an agent function
"""

from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Iterator, List, Optional, Union

__all__ = [
    "Case",
    "Eval",
    "EvalFailed",
    "EvalResults",
    "RunResult",
    "run",
]
__version__ = "0.1.0"

# Type alias for a custom scorer callable.
ScorerCallable = Callable[[str, str, Optional[str]], Union[bool, float]]
ScorerType = Union[str, ScorerCallable, None]


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class EvalFailed(Exception):
    """Raised by EvalResults.assert_all_passed() when any case failed.

    Attributes
    ----------
    failed_count : int
        Number of cases that failed.
    total_count : int
        Total number of cases run.
    results : EvalResults
        The full result set for inspection.
    """

    def __init__(self, failed_count: int, total_count: int, results: "EvalResults") -> None:
        self.failed_count = failed_count
        self.total_count = total_count
        self.results = results
        super().__init__(
            f"{failed_count}/{total_count} eval cases failed"
        )


# ---------------------------------------------------------------------------
# Case
# ---------------------------------------------------------------------------


@dataclass
class Case:
    """A single evaluation test case.

    Parameters
    ----------
    input : str
        The string passed to the agent function.
    expected : str or None
        Expected output. Interpretation depends on scorer.
        Not required when scorer is None.
    scorer : str, callable, or None
        How to evaluate the output against expected.

        Built-in string values:
            "exact"    — output.strip() == expected.strip() (case-sensitive)
            "contains" — expected.lower() in output.lower()
            "regex"    — re.search(expected, output, IGNORECASE)
            None / "none" — always passes (score 1.0); useful as baseline

        Callable signature: fn(input: str, output: str, expected: str | None) -> bool | float
        Return value is coerced to float (True -> 1.0, False -> 0.0).
        If the scorer itself raises, the run is treated as failed.

    label : str or None
        Optional human-readable label shown in summary output.
    timeout : float or None
        If set, the agent call must complete within this many seconds.
        Exceeding the timeout causes the run to fail with a TimeoutError.
        Default: no timeout.

    Examples
    --------
    >>> Case("2+2?", expected="4", scorer="exact")
    >>> Case("Capital?", expected="Paris", scorer="contains")
    >>> Case("Match?", expected=r"yes|wet", scorer="regex")
    >>> Case("Baseline", scorer=None)
    >>> Case("Custom", scorer=lambda i, o, e: len(o) < 500)
    """

    input: str
    expected: Optional[str] = None
    scorer: ScorerType = None
    label: Optional[str] = None
    timeout: Optional[float] = None

    def __post_init__(self) -> None:
        if isinstance(self.scorer, str):
            normalized = self.scorer.lower()
            valid = {"exact", "contains", "regex", "none"}
            if normalized not in valid:
                raise ValueError(
                    f"Unknown built-in scorer '{self.scorer}'. "
                    f"Valid options: {sorted(valid)}"
                )

    def display_name(self) -> str:
        """Return label if set, otherwise a truncated version of the input."""
        if self.label:
            return self.label
        truncated = self.input if len(self.input) <= 60 else self.input[:57] + "..."
        return truncated


# ---------------------------------------------------------------------------
# RunResult
# ---------------------------------------------------------------------------


@dataclass
class RunResult:
    """Result for a single case run.

    Attributes
    ----------
    case : Case
        The case that was run.
    output : str or None
        The string returned by the agent function.
        None if agent_fn raised an exception.
    passed : bool
        Whether the case passed (score >= 0.5 for float scorers,
        or the scorer returned True / truthy).
    score : float
        0.0 to 1.0. For boolean scorers this is exactly 0.0 or 1.0.
        For callable scorers that return a float, the raw float is used.
    error : str or None
        Exception message if agent_fn raised. None otherwise.
    duration_ms : float
        Wall-clock time for the agent call in milliseconds.
    """

    case: Case
    output: Optional[str]
    passed: bool
    score: float
    error: Optional[str]
    duration_ms: float


# ---------------------------------------------------------------------------
# EvalResults
# ---------------------------------------------------------------------------


class EvalResults:
    """Collection of RunResult objects returned by Eval.run().

    Supports iteration and len(). Summary and assertion helpers included.
    """

    def __init__(self, run_results: List[RunResult]) -> None:
        """Initialize with a list of RunResult objects."""
        self._results: List[RunResult] = run_results

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def score(self) -> float:
        """Mean score across all runs. 0.0 if no runs."""
        if not self._results:
            return 0.0
        return sum(r.score for r in self._results) / len(self._results)

    @property
    def passed(self) -> int:
        """Count of runs where passed=True."""
        return sum(1 for r in self._results if r.passed)

    @property
    def failed(self) -> int:
        """Count of runs where passed=False."""
        return sum(1 for r in self._results if not r.passed)

    @property
    def total(self) -> int:
        """Total number of runs."""
        return len(self._results)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def summary(self, verbose: bool = True) -> str:
        """Return a formatted summary string.

        Parameters
        ----------
        verbose : bool
            If True (default), list each case with pass/fail indicator.
            If False, return only the aggregate line.
        """
        score_pct = self.score * 100
        header = (
            f"Runs: {self.total} | "
            f"Passed: {self.passed} | "
            f"Failed: {self.failed} | "
            f"Score: {score_pct:.1f}%"
        )

        if not verbose or not self._results:
            return header

        lines = [header]
        for result in self._results:
            mark = "+" if result.passed else "-"
            name = result.case.display_name()
            detail = f"  [{mark}] {name}"
            if not result.passed:
                if result.error:
                    detail += f" (error: {result.error})"
                elif result.output is not None:
                    truncated = (
                        result.output
                        if len(result.output) <= 80
                        else result.output[:77] + "..."
                    )
                    detail += f" (got: {truncated!r})"
            lines.append(detail)

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Assertion
    # ------------------------------------------------------------------

    def assert_all_passed(self) -> None:
        """Raise EvalFailed if any case failed.

        Use this in CI to get a non-zero exit code on regressions:

            results = eval.run(agent)
            results.assert_all_passed()
        """
        if self.failed > 0:
            raise EvalFailed(self.failed, self.total, self)

    # ------------------------------------------------------------------
    # Sequence protocol
    # ------------------------------------------------------------------

    def __iter__(self) -> Iterator[RunResult]:
        """Iterate over RunResult objects."""
        return iter(self._results)

    def __len__(self) -> int:
        """Return total number of run results."""
        return len(self._results)


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------


def _apply_scorer(
    scorer: ScorerType,
    input_text: str,
    output: str,
    expected: Optional[str],
) -> float:
    """Apply a scorer and return a float score in 0.0-1.0.

    Raises
    ------
    ValueError
        If a built-in scorer is used without an expected value.
    Any exception from the callable scorer is propagated to the caller,
    which will catch it and record the run as failed.
    """
    if scorer is None or (isinstance(scorer, str) and scorer.lower() == "none"):
        return 1.0

    if isinstance(scorer, str):
        if expected is None:
            raise ValueError(
                f"Scorer '{scorer}' requires an expected value but none was provided."
            )
        name = scorer.lower()
        if name == "exact":
            return 1.0 if output.strip() == expected.strip() else 0.0
        if name == "contains":
            return 1.0 if expected.lower() in output.lower() else 0.0
        if name == "regex":
            return 1.0 if re.search(expected, output, re.IGNORECASE) else 0.0
        # Should not reach here after __post_init__ validation.
        raise ValueError(f"Unknown scorer '{scorer}'")

    # Callable scorer.
    raw = scorer(input_text, output, expected)
    if isinstance(raw, bool):
        return 1.0 if raw else 0.0
    return float(raw)


# ---------------------------------------------------------------------------
# Timeout execution helper
# ---------------------------------------------------------------------------


def _run_with_timeout(
    agent_fn: Callable[[str], str],
    input_text: str,
    timeout: Optional[float],
) -> tuple[Optional[str], Optional[str], float]:
    """Call agent_fn(input_text) with optional timeout.

    Returns
    -------
    (output, error, duration_ms)
        output is None if the call failed.
        error is the exception string if the call failed, else None.
        duration_ms is always set.
    """
    result_container: dict = {"output": None, "error": None}
    start = time.monotonic()

    if timeout is None:
        try:
            result_container["output"] = agent_fn(input_text)
        except Exception as exc:
            result_container["error"] = str(exc)
        duration_ms = (time.monotonic() - start) * 1000.0
        return result_container["output"], result_container["error"], duration_ms

    # Timeout path: run agent_fn in a daemon thread and join with timeout.
    def target() -> None:
        try:
            result_container["output"] = agent_fn(input_text)
        except Exception as exc:
            result_container["error"] = str(exc)

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(timeout=timeout)
    duration_ms = (time.monotonic() - start) * 1000.0

    if thread.is_alive():
        # Thread is still running — timed out.
        result_container["error"] = (
            f"TimeoutError: agent_fn did not return within {timeout}s"
        )

    return result_container["output"], result_container["error"], duration_ms


# ---------------------------------------------------------------------------
# Run a single case
# ---------------------------------------------------------------------------


def _run_case(
    case: Case,
    agent_fn: Callable[[str], str],
) -> RunResult:
    """Execute one case and return a RunResult.

    agent_fn exceptions are caught and recorded; they do not propagate.
    Scorer exceptions are also caught and recorded as failures.
    """
    output, error, duration_ms = _run_with_timeout(agent_fn, case.input, case.timeout)

    if error is not None:
        # Agent call failed — no output to score.
        return RunResult(
            case=case,
            output=None,
            passed=False,
            score=0.0,
            error=error,
            duration_ms=duration_ms,
        )

    # Agent returned — apply scorer.
    try:
        score = _apply_scorer(case.scorer, case.input, output, case.expected)  # type: ignore[arg-type]
    except Exception as exc:
        return RunResult(
            case=case,
            output=output,
            passed=False,
            score=0.0,
            error=f"ScorerError: {exc}",
            duration_ms=duration_ms,
        )

    # Clamp to [0.0, 1.0] for sanity; custom scorers might return >1.
    score = max(0.0, min(1.0, score))
    passed = score >= 0.5

    return RunResult(
        case=case,
        output=output,
        passed=passed,
        score=score,
        error=None,
        duration_ms=duration_ms,
    )


# ---------------------------------------------------------------------------
# Eval harness
# ---------------------------------------------------------------------------


class Eval:
    """Stateful evaluation harness. Accumulates cases and runs them together.

    Examples
    --------
    >>> e = Eval()
    >>> e.add(Case("2+2?", expected="4", scorer="exact"))
    >>> e.add(Case("Capital of France?", expected="Paris", scorer="contains"))
    >>> results = e.run(my_agent_fn)
    >>> print(results.summary())
    >>> results.assert_all_passed()
    """

    def __init__(self) -> None:
        """Initialize an empty Eval harness."""
        self._cases: List[Case] = []

    def add(self, case: Case) -> "Eval":
        """Add a Case to the harness. Returns self for chaining.

        Parameters
        ----------
        case : Case
            The test case to add.
        """
        self._cases.append(case)
        return self

    @property
    def cases(self) -> List[Case]:
        """The list of cases currently registered."""
        return list(self._cases)

    def run(self, agent_fn: Callable[[str], str]) -> EvalResults:
        """Run all registered cases against agent_fn.

        agent_fn must accept a single str and return a str.
        Exceptions from agent_fn are caught per-case and recorded as failures.

        Parameters
        ----------
        agent_fn : callable
            Any callable with signature (str) -> str.

        Returns
        -------
        EvalResults
            Full result set with pass/fail/score data.
        """
        run_results = [_run_case(case, agent_fn) for case in self._cases]
        return EvalResults(run_results)


# ---------------------------------------------------------------------------
# Standalone run() function
# ---------------------------------------------------------------------------


def run(
    agent_fn: Callable[[str], str],
    cases: List[Case],
) -> EvalResults:
    """Run a list of cases against agent_fn without creating an Eval object.

    Parameters
    ----------
    agent_fn : callable
        Any callable with signature (str) -> str.
    cases : list of Case
        Test cases to evaluate.

    Returns
    -------
    EvalResults
        Full result set.

    Examples
    --------
    >>> from agent_eval import run, Case
    >>> results = run(my_agent, [
    ...     Case("2+2?", expected="4", scorer="exact"),
    ...     Case("Capital?", expected="Paris", scorer="contains"),
    ... ])
    >>> print(results.summary())
    """
    run_results = [_run_case(case, agent_fn) for case in cases]
    return EvalResults(run_results)
