"""
Core retry logic for agent-retry.

Provides:
  - RetryConfig — configuration dataclass
  - retry() — decorator and direct-call wrapper (sync + async)
"""

import asyncio
import functools
import inspect
import random
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union

from .exceptions import RetryExhausted

# HTTP status codes that typically indicate a transient error worth retrying.
DEFAULT_RETRYABLE_STATUS_CODES: Tuple[int, ...] = (429, 500, 502, 503, 504)

# Sentinel: retry on any exception when no specific exceptions are specified.
_ANY_EXCEPTION = (Exception,)


@dataclass
class RetryConfig:
    """
    Configuration for retry behaviour.

    Parameters
    ----------
    max_attempts : int
        Total number of attempts (1 = no retries, just one call).
    base_delay : float
        Delay before the first retry, in seconds.
    max_delay : float
        Upper bound on the delay between attempts, in seconds.
    exponential_base : float
        Multiplier applied to the delay on each retry.
        delay_n = min(base_delay * exponential_base ** (n-1), max_delay)
    jitter : bool
        If True, adds uniform random jitter in [0, current_delay] to each
        delay to avoid thundering-herd on parallel agents.
    retryable_exceptions : tuple[type[Exception], ...]
        Only retry if the raised exception is an instance of one of these
        types. Default: retry on any exception.
    retryable_status_codes : tuple[int, ...]
        If an exception has a ``status_code`` or ``response.status_code``
        attribute matching one of these values, it is treated as retryable
        even if it doesn't match ``retryable_exceptions``.
    on_retry : callable, optional
        Called before each retry with (attempt: int, exception: Exception,
        delay: float). Useful for logging.
    on_failure : callable, optional
        Called when all attempts are exhausted with (attempts: int,
        exception: Exception).
    """

    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_exceptions: Tuple[Type[Exception], ...] = field(
        default_factory=lambda: _ANY_EXCEPTION  # type: ignore[return-value]
    )
    retryable_status_codes: Tuple[int, ...] = field(
        default_factory=lambda: DEFAULT_RETRYABLE_STATUS_CODES
    )
    on_retry: Optional[Callable[[int, Exception, float], None]] = None
    on_failure: Optional[Callable[[int, Exception], None]] = None


def _default_config() -> RetryConfig:
    return RetryConfig()


def _compute_delay(config: RetryConfig, attempt: int) -> float:
    """Return the delay (seconds) before attempt number ``attempt`` (1-indexed)."""
    raw = min(
        config.base_delay * (config.exponential_base ** (attempt - 1)),
        config.max_delay,
    )
    if config.jitter:
        raw = random.uniform(0.0, raw)
    return raw


def _is_retryable(exc: Exception, config: RetryConfig) -> bool:
    """Return True if the exception should trigger a retry."""
    if isinstance(exc, config.retryable_exceptions):
        return True
    # Check status_code attribute (common in httpx, requests, anthropic SDK).
    for attr in ("status_code", "code"):
        code = getattr(exc, attr, None)
        if isinstance(code, int) and code in config.retryable_status_codes:
            return True
    # Check exc.response.status_code (requests-style).
    response = getattr(exc, "response", None)
    if response is not None:
        code = getattr(response, "status_code", None)
        if isinstance(code, int) and code in config.retryable_status_codes:
            return True
    return False


def _parse_retry_after(exc: Exception) -> Optional[float]:
    """
    Look for a Retry-After value in the exception (as seconds).

    Returns the float seconds if found, else None.
    """
    for attr in ("retry_after", "headers"):
        val = getattr(exc, attr, None)
        if val is None:
            continue
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, dict):
            ra = val.get("Retry-After") or val.get("retry-after")
            if ra is not None:
                try:
                    return float(ra)
                except (TypeError, ValueError):
                    pass
    response = getattr(exc, "response", None)
    if response is not None:
        headers = getattr(response, "headers", {})
        if headers:
            ra = headers.get("Retry-After") or headers.get("retry-after")
            if ra is not None:
                try:
                    return float(ra)
                except (TypeError, ValueError):
                    pass
    return None


# ---------------------------------------------------------------------------
# Synchronous path
# ---------------------------------------------------------------------------

def _run_sync(fn: Callable, config: RetryConfig, args: tuple, kwargs: dict) -> Any:
    last_exc: Optional[Exception] = None

    for attempt in range(1, config.max_attempts + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if not _is_retryable(exc, config):
                raise  # non-retryable: pass through unchanged

            if attempt == config.max_attempts:
                break

            # Respect Retry-After header if present.
            delay = _parse_retry_after(exc) or _compute_delay(config, attempt)
            delay = min(delay, config.max_delay)

            if config.on_retry is not None:
                config.on_retry(attempt, exc, delay)

            time.sleep(delay)

    assert last_exc is not None
    if config.on_failure is not None:
        config.on_failure(attempt, last_exc)
    raise RetryExhausted(attempts=attempt, last_exception=last_exc)


# ---------------------------------------------------------------------------
# Asynchronous path
# ---------------------------------------------------------------------------

async def _run_async(fn: Callable, config: RetryConfig, args: tuple, kwargs: dict) -> Any:
    last_exc: Optional[Exception] = None

    for attempt in range(1, config.max_attempts + 1):
        try:
            return await fn(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if not _is_retryable(exc, config):
                raise  # non-retryable: pass through unchanged

            if attempt == config.max_attempts:
                break

            delay = _parse_retry_after(exc) or _compute_delay(config, attempt)
            delay = min(delay, config.max_delay)

            if config.on_retry is not None:
                config.on_retry(attempt, exc, delay)

            await asyncio.sleep(delay)

    assert last_exc is not None
    if config.on_failure is not None:
        config.on_failure(attempt, last_exc)
    raise RetryExhausted(attempts=attempt, last_exception=last_exc)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def retry(
    fn_or_config: Union[Callable, RetryConfig, None] = None,
    *,
    config: Optional[RetryConfig] = None,
    max_attempts: Optional[int] = None,
    base_delay: Optional[float] = None,
    max_delay: Optional[float] = None,
    exponential_base: Optional[float] = None,
    jitter: Optional[bool] = None,
    retryable_exceptions: Optional[Sequence[Type[Exception]]] = None,
    retryable_status_codes: Optional[Sequence[int]] = None,
    on_retry: Optional[Callable] = None,
    on_failure: Optional[Callable] = None,
) -> Any:
    """
    Retry decorator and direct-call wrapper for sync and async functions.

    Can be used in four ways::

        # 1. Decorator with defaults
        @retry
        def call_api(): ...

        # 2. Decorator with keyword arguments
        @retry(max_attempts=5, base_delay=2.0)
        def call_api(): ...

        # 3. Decorator with a RetryConfig
        @retry(config=RetryConfig(max_attempts=5))
        def call_api(): ...

        # 4. Direct call (wraps a single invocation)
        result = retry(call_api, max_attempts=5)()

    Works with both sync and async (``async def``) functions.

    Parameters
    ----------
    fn_or_config : callable or RetryConfig, optional
        When used as a bare decorator (``@retry``), this is the decorated
        function. When used as a factory (``@retry(...)``), this is None.
        Can also be a RetryConfig instance — retained for backward compat.
    config : RetryConfig, optional
        Full configuration object. Keyword args below override individual
        fields when config is also provided.
    max_attempts, base_delay, max_delay, exponential_base, jitter,
    retryable_exceptions, retryable_status_codes, on_retry, on_failure :
        Convenience shorthands — equivalent to setting fields on RetryConfig.

    Returns
    -------
    Any
        When used as a decorator, returns the wrapped function. When called
        directly with a function, returns the result of calling that function
        with retry logic applied.

    Raises
    ------
    RetryExhausted
        If all attempts fail.
    """

    def _build_config() -> RetryConfig:
        base = config or RetryConfig()
        kw: dict = {}
        if max_attempts is not None:
            kw["max_attempts"] = max_attempts
        if base_delay is not None:
            kw["base_delay"] = base_delay
        if max_delay is not None:
            kw["max_delay"] = max_delay
        if exponential_base is not None:
            kw["exponential_base"] = exponential_base
        if jitter is not None:
            kw["jitter"] = jitter
        if retryable_exceptions is not None:
            kw["retryable_exceptions"] = tuple(retryable_exceptions)
        if retryable_status_codes is not None:
            kw["retryable_status_codes"] = tuple(retryable_status_codes)
        if on_retry is not None:
            kw["on_retry"] = on_retry
        if on_failure is not None:
            kw["on_failure"] = on_failure
        if kw:
            import dataclasses
            return dataclasses.replace(base, **kw)
        return base

    def _wrap(fn: Callable) -> Callable:
        cfg = _build_config()
        if inspect.iscoroutinefunction(fn):
            @functools.wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await _run_async(fn, cfg, args, kwargs)
            return async_wrapper
        else:
            @functools.wraps(fn)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return _run_sync(fn, cfg, args, kwargs)
            return sync_wrapper

    # Case 1: @retry — bare decorator, fn_or_config is the function.
    if callable(fn_or_config) and not isinstance(fn_or_config, RetryConfig):
        return _wrap(fn_or_config)

    # Case 2: @retry(...) or @retry(config=...) — factory call.
    # fn_or_config is None or a RetryConfig.
    if isinstance(fn_or_config, RetryConfig) and config is None:
        # Allow @retry(my_config) shorthand — reassign via closure trick.
        def _wrap_with_cfg(fn: Callable) -> Callable:
            cfg = fn_or_config
            if inspect.iscoroutinefunction(fn):
                @functools.wraps(fn)
                async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                    return await _run_async(fn, cfg, args, kwargs)
                return async_wrapper
            else:
                @functools.wraps(fn)
                def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                    return _run_sync(fn, cfg, args, kwargs)
                return sync_wrapper
        return _wrap_with_cfg

    return _wrap
