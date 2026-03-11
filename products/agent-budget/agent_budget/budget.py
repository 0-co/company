"""budget.py — BudgetEnforcer and BudgetExceeded."""

import sys
import warnings
from .pricing import get_cost


class BudgetExceeded(Exception):
    """Raised when a budget limit (tokens or cost) is exceeded.

    Attributes:
        limit_type  -- "tokens" or "cost"
        limit       -- the configured limit value
        used        -- value at the time of the violation
        model       -- model that triggered the violation (may be None)
        msg         -- human-readable description
    """

    def __init__(self, limit_type: str, limit, used, model=None):
        self.limit_type = limit_type
        self.limit = limit
        self.used = used
        self.model = model
        if limit_type == "tokens":
            self.msg = (
                f"Token limit exceeded: used {used:,} / {limit:,} tokens"
                + (f" (model: {model})" if model else "")
            )
        else:
            self.msg = (
                f"Cost limit exceeded: used ${used:.4f} / ${limit:.2f}"
                + (f" (model: {model})" if model else "")
            )
        super().__init__(self.msg)


class BudgetEnforcer:
    """Track token and/or cost usage across API calls and enforce limits.

    Parameters
    ----------
    max_tokens:     stop when total tokens (input + output) reaches this value.
    max_cost_usd:   stop when total cost reaches this value (USD).
    warn_at:        fraction of the limit at which to print a warning (default 0.8).
    model:          default model name used for cost calculations when the call
                    does not specify one.
    """

    def __init__(
        self,
        max_tokens=None,
        max_cost_usd=None,
        warn_at: float = 0.8,
        model: str = "claude-sonnet-4-6",
    ):
        if max_tokens is None and max_cost_usd is None:
            raise ValueError("Provide at least one of max_tokens or max_cost_usd.")

        self.max_tokens = max_tokens
        self.max_cost_usd = max_cost_usd
        self.warn_at = warn_at
        self.model = model

        self._used_tokens: int = 0
        self._used_cost_usd: float = 0.0

        # Track whether we've already emitted the warn threshold warning so we
        # don't spam stderr on every subsequent call.
        self._token_warn_fired: bool = False
        self._cost_warn_fired: bool = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def used_tokens(self) -> int:
        return self._used_tokens

    @property
    def used_cost_usd(self) -> float:
        return self._used_cost_usd

    @property
    def remaining_tokens(self):
        if self.max_tokens is None:
            return None
        return max(0, self.max_tokens - self._used_tokens)

    @property
    def remaining_cost_usd(self):
        if self.max_cost_usd is None:
            return None
        return max(0.0, self.max_cost_usd - self._used_cost_usd)

    # ------------------------------------------------------------------
    # Core tracking logic
    # ------------------------------------------------------------------

    def track(self, input_tokens: int, output_tokens: int, model=None):
        """Update counters for one API call, check limits, raise if exceeded.

        Call this after each API response.  Raises BudgetExceeded if any
        configured limit is crossed.  Emits a warning to stderr when usage
        reaches the warn_at fraction of a limit (fires once per threshold
        crossing).

        Parameters
        ----------
        input_tokens:  prompt tokens consumed.
        output_tokens: completion tokens produced.
        model:         model string; falls back to self.model if None.
        """
        model = model or self.model
        total_new_tokens = input_tokens + output_tokens
        call_cost = get_cost(model, input_tokens, output_tokens)

        self._used_tokens += total_new_tokens
        self._used_cost_usd += call_cost

        # Check hard limits — raise immediately.
        if self.max_tokens is not None and self._used_tokens >= self.max_tokens:
            raise BudgetExceeded(
                "tokens", self.max_tokens, self._used_tokens, model
            )
        if self.max_cost_usd is not None and self._used_cost_usd >= self.max_cost_usd:
            raise BudgetExceeded(
                "cost", self.max_cost_usd, self._used_cost_usd, model
            )

        # Check warn thresholds — print once per crossing.
        if self.max_tokens is not None and not self._token_warn_fired:
            ratio = self._used_tokens / self.max_tokens
            if ratio >= self.warn_at:
                self._token_warn_fired = True
                print(
                    f"[agent-budget] WARNING: token usage at {ratio*100:.1f}%"
                    f" ({self._used_tokens:,} / {self.max_tokens:,})",
                    file=sys.stderr,
                )

        if self.max_cost_usd is not None and not self._cost_warn_fired:
            ratio = self._used_cost_usd / self.max_cost_usd
            if ratio >= self.warn_at:
                self._cost_warn_fired = True
                print(
                    f"[agent-budget] WARNING: cost usage at {ratio*100:.1f}%"
                    f" (${self._used_cost_usd:.4f} / ${self.max_cost_usd:.2f})",
                    file=sys.stderr,
                )

    def reset(self):
        """Reset all counters and warn flags.

        Useful in rate-limited scenarios where you want a fresh budget window
        without creating a new enforcer.
        """
        self._used_tokens = 0
        self._used_cost_usd = 0.0
        self._token_warn_fired = False
        self._cost_warn_fired = False

    # ------------------------------------------------------------------
    # Status display
    # ------------------------------------------------------------------

    def status(self) -> str:
        """Return a formatted string showing current usage vs limits."""
        lines = []

        if self.max_tokens is not None:
            pct = (self._used_tokens / self.max_tokens) * 100
            lines.append(
                f"Tokens: {self._used_tokens:,} / {self.max_tokens:,} ({pct:.1f}%)"
            )
        else:
            lines.append(f"Tokens: {self._used_tokens:,} (no limit)")

        if self.max_cost_usd is not None:
            pct = (self._used_cost_usd / self.max_cost_usd) * 100
            lines.append(
                f"Cost:   ${self._used_cost_usd:.4f} / ${self.max_cost_usd:.2f} ({pct:.1f}%)"
            )
        else:
            lines.append(f"Cost:   ${self._used_cost_usd:.4f} (no limit)")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Client wrapping
    # ------------------------------------------------------------------

    def wrap(self, client):
        """Return a budget-aware proxy for an Anthropic or OpenAI client.

        The proxy is transparent — all attributes not explicitly overridden
        are forwarded to the underlying client.

        If the client is neither an Anthropic nor OpenAI client, it is returned
        unwrapped with a warning.
        """
        client_type = type(client).__name__
        module = type(client).__module__ or ""

        if "anthropic" in module:
            return _AnthropicProxy(client, self)

        if "openai" in module:
            return _OpenAIProxy(client, self)

        # Unknown client type — warn and return as-is so code still runs.
        warnings.warn(
            f"[agent-budget] Unknown client type '{client_type}' from module "
            f"'{module}'. Returning client unwrapped — no budget tracking.",
            stacklevel=2,
        )
        return client


# ---------------------------------------------------------------------------
# Anthropic proxy
# ---------------------------------------------------------------------------

class _AnthropicProxy:
    """Transparent proxy around an anthropic.Anthropic client."""

    def __init__(self, client, enforcer: BudgetEnforcer):
        self._client = client
        self._enforcer = enforcer
        self.messages = _AnthropicMessagesProxy(client.messages, enforcer)

    def __getattr__(self, name):
        return getattr(self._client, name)


class _AnthropicMessagesProxy:
    """Proxy for the .messages namespace of an Anthropic client."""

    def __init__(self, messages, enforcer: BudgetEnforcer):
        self._messages = messages
        self._enforcer = enforcer

    def create(self, *args, **kwargs):
        response = self._messages.create(*args, **kwargs)
        if hasattr(response, "usage") and response.usage is not None:
            self._enforcer.track(
                response.usage.input_tokens,
                response.usage.output_tokens,
                kwargs.get("model"),
            )
        return response

    def stream(self, *args, **kwargs):
        """Wrap the streaming context manager.

        Usage:
            with client.messages.stream(...) as stream:
                for text in stream.text_stream:
                    ...
                final = stream.get_final_message()
        """
        return _AnthropicStreamProxy(
            self._messages.stream(*args, **kwargs),
            self._enforcer,
            kwargs.get("model"),
        )

    def __getattr__(self, name):
        return getattr(self._messages, name)


class _AnthropicStreamProxy:
    """Wrap the Anthropic streaming context manager to track usage on exit."""

    def __init__(self, stream_cm, enforcer: BudgetEnforcer, model=None):
        self._stream_cm = stream_cm
        self._enforcer = enforcer
        self._model = model
        self._stream = None

    def __enter__(self):
        self._stream = self._stream_cm.__enter__()
        return self._stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = self._stream_cm.__exit__(exc_type, exc_val, exc_tb)
        # Only track on clean exit; if an exception propagated, the stream
        # may not have a final message with usage.
        if exc_type is None and self._stream is not None:
            try:
                msg = self._stream.get_final_message()
                if hasattr(msg, "usage") and msg.usage is not None:
                    self._enforcer.track(
                        msg.usage.input_tokens,
                        msg.usage.output_tokens,
                        self._model,
                    )
            except Exception:
                pass  # best-effort; don't shadow original exception
        return result

    def __getattr__(self, name):
        return getattr(self._stream_cm, name)


# ---------------------------------------------------------------------------
# OpenAI proxy
# ---------------------------------------------------------------------------

class _OpenAIProxy:
    """Transparent proxy around an openai.OpenAI (or AsyncOpenAI) client."""

    def __init__(self, client, enforcer: BudgetEnforcer):
        self._client = client
        self._enforcer = enforcer
        self.chat = _OpenAIChatProxy(client.chat, enforcer)

    def __getattr__(self, name):
        return getattr(self._client, name)


class _OpenAIChatProxy:
    """Proxy for the .chat namespace."""

    def __init__(self, chat, enforcer: BudgetEnforcer):
        self._chat = chat
        self._enforcer = enforcer
        self.completions = _OpenAICompletionsProxy(chat.completions, enforcer)

    def __getattr__(self, name):
        return getattr(self._chat, name)


class _OpenAICompletionsProxy:
    """Proxy for .chat.completions."""

    def __init__(self, completions, enforcer: BudgetEnforcer):
        self._completions = completions
        self._enforcer = enforcer

    def create(self, *args, **kwargs):
        response = self._completions.create(*args, **kwargs)
        if hasattr(response, "usage") and response.usage is not None:
            self._enforcer.track(
                response.usage.prompt_tokens,
                response.usage.completion_tokens,
                kwargs.get("model"),
            )
        return response

    def __getattr__(self, name):
        return getattr(self._completions, name)
