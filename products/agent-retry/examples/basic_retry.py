"""
agent-retry basic examples.

Run from the products/agent-retry directory:
  python examples/basic_retry.py
"""

import sys
import time
from pathlib import Path

# Allow running without installing.
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_retry import RetryConfig, RetryExhausted, retry

print("=== agent-retry basic examples ===\n")


# ── Example 1: bare @retry ────────────────────────────────────────────────────
_call_count_1 = 0

@retry
def always_fails():
    global _call_count_1
    _call_count_1 += 1
    raise ConnectionError("network down")

print("Example 1: bare @retry (default 3 attempts, exponential backoff)")
try:
    always_fails()
except RetryExhausted as e:
    print(f"  RetryExhausted: {e.attempts} attempts, last={type(e.last_exception).__name__}")
print()


# ── Example 2: succeed on 3rd attempt ────────────────────────────────────────
_call_count_2 = 0

@retry(max_attempts=5, base_delay=0.01, jitter=False)
def succeeds_on_third():
    global _call_count_2
    _call_count_2 += 1
    if _call_count_2 < 3:
        raise OSError("not ready yet")
    return f"success on attempt {_call_count_2}"

result = succeeds_on_third()
print(f"Example 2: succeed on attempt 3: {result!r}")
print()


# ── Example 3: RetryConfig with on_retry callback ────────────────────────────
_call_count_3 = 0
_retry_log = []

config = RetryConfig(
    max_attempts=4,
    base_delay=0.01,
    max_delay=1.0,
    jitter=False,
    on_retry=lambda attempt, exc, delay: _retry_log.append(
        f"attempt {attempt} failed ({exc}), waiting {delay:.3f}s"
    ),
    on_failure=lambda attempts, exc: _retry_log.append(f"gave up after {attempts}"),
)

@retry(config=config)
def flaky_api():
    global _call_count_3
    _call_count_3 += 1
    if _call_count_3 <= 3:
        raise ValueError("flaky")
    return "ok"

result = flaky_api()
print("Example 3: RetryConfig with on_retry callback:")
for entry in _retry_log:
    print(f"  {entry}")
print(f"  Final result: {result!r}")
print()


# ── Example 4: retryable_status_codes ────────────────────────────────────────
_call_count_4 = 0

class FakeRateLimitError(Exception):
    status_code = 429

@retry(
    max_attempts=3,
    base_delay=0.01,
    retryable_exceptions=(FakeRateLimitError,),
    retryable_status_codes=(429,),
)
def rate_limited_call():
    global _call_count_4
    _call_count_4 += 1
    if _call_count_4 < 2:
        raise FakeRateLimitError("429 rate limited")
    return f"success after {_call_count_4} attempts"

result = rate_limited_call()
print(f"Example 4: retryable_status_codes (429): {result!r}")
print()


# ── Example 5: non-retryable exception passes through immediately ─────────────
_call_count_5 = 0

@retry(
    max_attempts=5,
    base_delay=0.01,
    retryable_exceptions=(ConnectionError,),
)
def non_retryable():
    global _call_count_5
    _call_count_5 += 1
    raise ValueError("not retryable")

print("Example 5: non-retryable exception passes through immediately")
try:
    non_retryable()
except RetryExhausted as e:
    print(f"  RetryExhausted with {_call_count_5} attempt(s): {e.last_exception}")
except ValueError as e:
    print(f"  ValueError passed through after {_call_count_5} attempt(s): {e}")
print()


# ── Example 6: async retry ────────────────────────────────────────────────────
import asyncio

_call_count_6 = 0

@retry(max_attempts=3, base_delay=0.01, jitter=False)
async def async_flaky():
    global _call_count_6
    _call_count_6 += 1
    if _call_count_6 < 2:
        raise TimeoutError("async timeout")
    return f"async ok on attempt {_call_count_6}"

result = asyncio.run(async_flaky())
print(f"Example 6: async retry: {result!r}")
print()

print("All examples passed.")
