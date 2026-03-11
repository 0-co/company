"""context.py — ContextManager, trim(), and ContextOverflow."""

from __future__ import annotations

from typing import Callable, List, Optional

# A message dict as used by Anthropic/OpenAI: {"role": ..., "content": ...}
Message = dict


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: one token per four characters.

    This is a heuristic used across the industry. Real tokenizers vary by
    model, but chars/4 gives a close enough approximation for pruning
    decisions without any external dependencies.
    """
    return len(text) // 4


def _message_tokens(message: Message) -> int:
    """Return token estimate for a single message dict."""
    content = message.get("content", "")
    if isinstance(content, list):
        # Anthropic multi-part content: list of {"type": ..., "text": ...}
        text = " ".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        )
    else:
        text = str(content)
    return _estimate_tokens(text)


def _total_tokens(messages: List[Message]) -> int:
    """Sum token estimates across a list of messages."""
    return sum(_message_tokens(m) for m in messages)


def _apply_sliding_window(
    messages: List[Message],
    max_turns: int,
    system_message: Optional[Message],
) -> List[Message]:
    """Keep the last max_turns messages, always preserving the system message.

    A 'turn' here is one message (not a user+assistant pair), to keep the
    implementation simple and avoid partial-pair edge cases.
    """
    trimmed = messages[-max_turns:] if len(messages) > max_turns else list(messages)

    if system_message is not None:
        return [system_message] + trimmed
    return trimmed


def _apply_token_budget(
    messages: List[Message],
    max_tokens: int,
    system_message: Optional[Message],
) -> List[Message]:
    """Keep as many messages as fit within max_tokens, newest first.

    Always keeps the system message (not counted against the budget).
    Walks the message list from newest to oldest, including each message
    until the budget runs out.
    """
    system_tokens = _message_tokens(system_message) if system_message is not None else 0
    remaining = max_tokens - system_tokens

    kept: List[Message] = []
    for message in reversed(messages):
        cost = _message_tokens(message)
        if cost <= remaining:
            kept.append(message)
            remaining -= cost
        else:
            # Once we can't fit the next message, stop — preserves ordering.
            break

    kept.reverse()

    if system_message is not None:
        return [system_message] + kept
    return kept


def _apply_compress(
    messages: List[Message],
    max_turns: int,
    system_message: Optional[Message],
    summarizer: Optional[Callable[[List[Message]], str]],
    keep_first: int,
    keep_last: int,
) -> List[Message]:
    """Keep first N + last N messages, summarize the middle.

    If no summarizer is provided, falls back to sliding window (keep last
    max_turns messages).

    The summary is inserted as an assistant message so it looks natural in
    the conversation context rather than as a pseudo-system injection.
    """
    total = len(messages)
    middle_start = keep_first
    middle_end = total - keep_last

    # Not enough messages to warrant compression — return everything.
    if middle_end <= middle_start:
        if system_message is not None:
            return [system_message] + list(messages)
        return list(messages)

    if summarizer is None:
        # Fall back: sliding window
        return _apply_sliding_window(messages, max_turns, system_message)

    first_block = messages[:keep_first]
    middle_block = messages[middle_start:middle_end]
    last_block = messages[middle_end:]

    summary_text = summarizer(middle_block)
    summary_message: Message = {
        "role": "assistant",
        "content": f"[Summary of {len(middle_block)} earlier messages]: {summary_text}",
    }

    result = first_block + [summary_message] + last_block
    if system_message is not None:
        return [system_message] + result
    return result


def trim(
    messages: List[Message],
    max_tokens: Optional[int] = None,
    max_turns: Optional[int] = None,
    strategy: Optional[str] = None,
    summarizer: Optional[Callable[[List[Message]], str]] = None,
    keep_first: int = 2,
    keep_last: int = 4,
    system: Optional[str] = None,
) -> List[Message]:
    """Trim a list of messages to fit within the given constraints.

    This is the stateless functional interface. For stateful usage across
    multiple turns, use ContextManager.

    Parameters
    ----------
    messages:
        List of message dicts ({"role": ..., "content": ...}).
    max_tokens:
        Maximum token budget (chars/4 heuristic). Triggers token_budget
        strategy by default.
    max_turns:
        Maximum number of messages to retain. Triggers sliding_window
        strategy by default.
    strategy:
        One of "sliding_window", "token_budget", or "compress". Inferred
        from the limit type if not specified.
    summarizer:
        Callable used by the compress strategy. Receives a list of messages
        and returns a string summary. Required for compress to actually
        compress; falls back to sliding_window without it.
    keep_first:
        Number of messages to preserve at the start in compress mode.
    keep_last:
        Number of messages to preserve at the end in compress mode.
    system:
        Optional system prompt text. If provided, a system message is always
        prepended and never trimmed.

    Returns
    -------
    List of message dicts trimmed to fit the constraints.
    """
    if not messages:
        if system is not None:
            return [{"role": "system", "content": system}]
        return []

    system_message: Optional[Message] = (
        {"role": "system", "content": system} if system is not None else None
    )

    # Filter out any pre-existing system messages from the input to avoid
    # duplication when a system param is given.
    non_system = [m for m in messages if m.get("role") != "system"]

    # Determine effective strategy.
    effective_strategy = strategy
    if effective_strategy is None:
        if max_tokens is not None:
            effective_strategy = "token_budget"
        elif max_turns is not None:
            effective_strategy = "sliding_window"
        else:
            effective_strategy = "sliding_window"

    effective_max_turns = max_turns if max_turns is not None else 20

    if effective_strategy == "token_budget":
        if max_tokens is None:
            # Fallback: use sliding window with default max_turns
            return _apply_sliding_window(non_system, effective_max_turns, system_message)
        return _apply_token_budget(non_system, max_tokens, system_message)

    if effective_strategy == "compress":
        return _apply_compress(
            non_system,
            effective_max_turns,
            system_message,
            summarizer,
            keep_first,
            keep_last,
        )

    # Default: sliding_window
    return _apply_sliding_window(non_system, effective_max_turns, system_message)


class ContextOverflow(Exception):
    """Raised when raise_on_overflow=True and the context exceeds its limit.

    Attributes
    ----------
    limit_type:
        "tokens" or "turns"
    limit:
        The configured limit value.
    current:
        The current value at the time of the violation.
    msg:
        Human-readable description (also available via str(e)).
    """

    def __init__(self, limit_type: str, limit: int, current: int):
        self.limit_type = limit_type
        self.limit = limit
        self.current = current
        if limit_type == "tokens":
            self.msg = (
                f"Context token limit exceeded: {current:,} tokens in window "
                f"(limit: {limit:,})"
            )
        else:
            self.msg = (
                f"Context turn limit exceeded: {current} turns in window "
                f"(limit: {limit})"
            )
        super().__init__(self.msg)


class ContextManager:
    """Manage LLM conversation history to prevent context rot.

    Maintains a running message history and applies a pruning strategy
    automatically on each add(). The get() method returns the current
    trimmed window ready to pass directly to an LLM client.

    Parameters
    ----------
    max_turns:
        Maximum number of messages to keep in the window. Default: 20.
    max_tokens:
        Maximum token budget for the window (chars/4 heuristic).
    strategy:
        Pruning strategy. One of:
          - "sliding_window": keep last max_turns messages (default when
            max_turns is set).
          - "token_budget": keep newest messages that fit within max_tokens
            (default when max_tokens is set).
          - "compress": keep first keep_first + last keep_last messages,
            summarize the middle using the summarizer callable.
    summarizer:
        Callable for compress strategy: fn(messages: list[dict]) -> str.
        Falls back to sliding_window if not provided.
    keep_first:
        Messages to preserve at start in compress mode. Default: 2.
    keep_last:
        Messages to preserve at end in compress mode. Default: 4.
    system:
        System prompt text. Always prepended in get(), never trimmed.
    raise_on_overflow:
        If True, raises ContextOverflow when a message would exceed limits
        instead of silently pruning. Default: False.
    """

    def __init__(
        self,
        max_turns: Optional[int] = None,
        max_tokens: Optional[int] = None,
        strategy: Optional[str] = None,
        summarizer: Optional[Callable[[List[Message]], str]] = None,
        keep_first: int = 2,
        keep_last: int = 4,
        system: Optional[str] = None,
        raise_on_overflow: bool = False,
    ):
        self._max_turns = max_turns
        self._max_tokens = max_tokens
        self._strategy = strategy
        self._summarizer = summarizer
        self._keep_first = keep_first
        self._keep_last = keep_last
        self._system = system
        self._raise_on_overflow = raise_on_overflow

        # Full unbounded history — all messages ever added.
        self._history: List[Message] = []

        # Determine effective strategy for internal use.
        self._effective_strategy = strategy
        if self._effective_strategy is None:
            if max_tokens is not None:
                self._effective_strategy = "token_budget"
            elif max_turns is not None:
                self._effective_strategy = "sliding_window"
            else:
                self._effective_strategy = "sliding_window"

        # Effective max_turns fallback.
        self._effective_max_turns = max_turns if max_turns is not None else 20

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def total_turns(self) -> int:
        """Total number of messages added (not trimmed) over the lifetime."""
        return len(self._history)

    @property
    def current_turns(self) -> int:
        """Number of messages in the current trimmed window."""
        window = self._current_window()
        return sum(1 for m in window if m.get("role") != "system")

    @property
    def tokens_estimate(self) -> int:
        """Rough token estimate (chars/4) of the current trimmed window."""
        return _total_tokens(self._current_window())

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, role: str, content: str) -> None:
        """Append a message to the conversation history.

        Parameters
        ----------
        role:
            Message role: "user", "assistant", or "system". Adding a system
            message via add() is allowed but the system parameter on __init__
            is the preferred way to set a persistent system prompt.
        content:
            Message text content.
        """
        self._history.append({"role": role, "content": content})

        if self._raise_on_overflow:
            self._check_overflow()

    def get(self) -> List[Message]:
        """Return the current message window, trimmed to fit the configured limits.

        The system prompt (if set) is always prepended and never trimmed.
        Returns a new list — safe to mutate.
        """
        return self._current_window()

    def clear(self) -> None:
        """Clear all history. The system prompt is retained."""
        self._history = []

    def reset(self) -> None:
        """Alias for clear()."""
        self.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _current_window(self) -> List[Message]:
        """Compute and return the trimmed window for current history."""
        return trim(
            self._history,
            max_tokens=self._max_tokens,
            max_turns=self._effective_max_turns,
            strategy=self._effective_strategy,
            summarizer=self._summarizer,
            keep_first=self._keep_first,
            keep_last=self._keep_last,
            system=self._system,
        )

    def _check_overflow(self) -> None:
        """Raise ContextOverflow if the current window exceeds limits.

        Called after each add() when raise_on_overflow=True.
        The check is against the UNCOMPRESSED history (before trimming),
        so it fires the moment you would need to start pruning.
        """
        # Count non-system messages in raw history.
        non_system = [m for m in self._history if m.get("role") != "system"]

        if self._max_turns is not None and len(non_system) > self._max_turns:
            raise ContextOverflow("turns", self._max_turns, len(non_system))

        if self._max_tokens is not None:
            current_tokens = _total_tokens(non_system)
            if current_tokens > self._max_tokens:
                raise ContextOverflow("tokens", self._max_tokens, current_tokens)
