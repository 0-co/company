"""agent-cache — core cache implementation."""

import hashlib
import json
import os
import time
import types
from pathlib import Path
from typing import Any, Dict, Optional

# Params that affect the response (cacheable)
_CACHEABLE_PARAMS = frozenset({
    "temperature", "max_tokens", "max_tokens_to_sample",
    "top_p", "top_k", "stop_sequences", "stop",
    "system", "n", "frequency_penalty", "presence_penalty",
    "seed", "logprobs", "top_logprobs",
})

# Per-million-token pricing (input, output) — same table as agent-budget
_MODEL_PRICES = {
    "claude-opus-4-6":       (15.00, 75.00),
    "claude-sonnet-4-6":     (3.00,  15.00),
    "claude-haiku-4-5-20251001": (0.80, 4.00),
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-3-5-haiku-20241022":  (0.80, 4.00),
    "claude-3-opus-20240229":     (15.00, 75.00),
    "gpt-4o":                (2.50,  10.00),
    "gpt-4o-mini":           (0.15,   0.60),
    "gpt-4-turbo":           (10.00, 30.00),
    "gpt-3.5-turbo":         (0.50,  1.50),
    "o1":                    (15.00, 60.00),
    "o1-mini":               (3.00,  12.00),
}


class CacheStats:
    """Cache statistics."""

    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.entries: int = 0
        self.input_tokens_saved: int = 0
        self.output_tokens_saved: int = 0
        self.cost_saved_usd: float = 0.0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def __repr__(self) -> str:
        return (
            f"CacheStats(hits={self.hits}, misses={self.misses}, "
            f"hit_rate={self.hit_rate:.1%}, "
            f"cost_saved=${self.cost_saved_usd:.4f})"
        )


class CacheEntry:
    """A single cache entry."""

    def __init__(self, response: Dict, model: str, created_at: float,
                 input_tokens: int = 0, output_tokens: int = 0):
        self.response = response
        self.model = model
        self.created_at = created_at
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.hits = 0

    def to_dict(self) -> Dict:
        return {
            "response": self.response,
            "model": self.model,
            "created_at": self.created_at,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "hits": self.hits,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "CacheEntry":
        entry = cls(
            response=d["response"],
            model=d.get("model", ""),
            created_at=d.get("created_at", 0.0),
            input_tokens=d.get("input_tokens", 0),
            output_tokens=d.get("output_tokens", 0),
        )
        entry.hits = d.get("hits", 0)
        return entry


def _dict_to_namespace(obj: Any) -> Any:
    """Recursively convert dicts to SimpleNamespace for attribute access."""
    if isinstance(obj, dict):
        return types.SimpleNamespace(**{k: _dict_to_namespace(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [_dict_to_namespace(i) for i in obj]
    return obj


def _serialize_response(response: Any) -> Dict:
    """Serialize an Anthropic or OpenAI response to a JSON-safe dict."""
    # Try pydantic v2 (Anthropic/OpenAI SDKs)
    if hasattr(response, "model_dump"):
        return response.model_dump()
    # Try pydantic v1
    if hasattr(response, "dict"):
        return response.dict()
    # Try __dict__
    if hasattr(response, "__dict__"):
        return json.loads(json.dumps(vars(response), default=str))
    raise TypeError(f"Cannot serialize response of type {type(response)}")


def _extract_token_counts(response_dict: Dict) -> tuple[int, int]:
    """Extract (input_tokens, output_tokens) from a serialized response dict."""
    # Anthropic: response.usage.input_tokens / output_tokens
    usage = response_dict.get("usage", {})
    if isinstance(usage, dict):
        inp = usage.get("input_tokens", 0) or 0
        out = usage.get("output_tokens", 0) or 0
        if inp or out:
            return int(inp), int(out)
        # OpenAI: usage.prompt_tokens / completion_tokens
        inp = usage.get("prompt_tokens", 0) or 0
        out = usage.get("completion_tokens", 0) or 0
        return int(inp), int(out)
    return 0, 0


def _cost_for(model: str, input_tokens: int, output_tokens: int) -> float:
    prices = _MODEL_PRICES.get(model, (0.0, 0.0))
    return (input_tokens * prices[0] + output_tokens * prices[1]) / 1_000_000


class ResponseCache:
    """
    LLM response cache. Wraps Anthropic or OpenAI clients to avoid
    duplicate API calls and track cost savings.

    Args:
        path: Path to cache file (default: ~/.cache/agent-cache/cache.json)
        ttl: Time-to-live in seconds. None = cache forever.
        max_entries: Max number of cached responses. Oldest evicted first.
    """

    def __init__(
        self,
        path: Optional[str] = None,
        ttl: Optional[int] = None,
        max_entries: int = 10_000,
    ):
        if path is None:
            path = os.path.expanduser("~/.cache/agent-cache/cache.json")
        self._path = Path(path)
        self._ttl = ttl
        self._max_entries = max_entries
        self._data: Dict[str, CacheEntry] = {}
        self._stats = CacheStats()
        self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def wrap(self, client: Any) -> Any:
        """
        Wrap an Anthropic or OpenAI client. Returns a cached client.

        Usage:
            client = ResponseCache().wrap(anthropic.Anthropic())
            response = client.messages.create(...)  # cached
        """
        client_type = type(client).__name__
        module = type(client).__module__

        if "anthropic" in module:
            from .wrappers import CachedAnthropicClient
            return CachedAnthropicClient(client, self)
        if "openai" in module:
            from .wrappers import CachedOpenAIClient
            return CachedOpenAIClient(client, self)

        raise ValueError(
            f"Unknown client type: {client_type}. "
            "Pass an anthropic.Anthropic or openai.OpenAI instance."
        )

    def get(self, key: str) -> Optional[Any]:
        """
        Look up a cache key. Returns a namespace object (attribute-accessible)
        if found, or None if missing/expired.
        """
        entry = self._data.get(key)
        if entry is None:
            self._stats.misses += 1
            return None

        if self._ttl is not None:
            if time.time() - entry.created_at > self._ttl:
                del self._data[key]
                self._stats.misses += 1
                return None

        entry.hits += 1
        self._stats.hits += 1
        self._stats.input_tokens_saved += entry.input_tokens
        self._stats.output_tokens_saved += entry.output_tokens
        self._stats.cost_saved_usd += _cost_for(
            entry.model, entry.input_tokens, entry.output_tokens
        )
        return _dict_to_namespace(entry.response)

    def set(self, key: str, response: Any, model: str = "") -> None:
        """
        Store a response under a key. Accepts raw SDK response objects or
        pre-serialized dicts.
        """
        if isinstance(response, dict):
            response_dict = response
        else:
            response_dict = _serialize_response(response)

        input_tokens, output_tokens = _extract_token_counts(response_dict)
        entry = CacheEntry(
            response=response_dict,
            model=model,
            created_at=time.time(),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
        self._data[key] = entry
        self._stats.entries = len(self._data)

        if len(self._data) > self._max_entries:
            oldest = min(self._data, key=lambda k: self._data[k].created_at)
            del self._data[oldest]

        self._save()

    def make_key(self, model: str, messages: Any, **params: Any) -> str:
        """Compute a deterministic cache key for a request."""
        cacheable = {k: v for k, v in params.items() if k in _CACHEABLE_PARAMS}
        key_obj = {
            "model": model,
            "messages": messages,
            **dict(sorted(cacheable.items())),
        }
        serialized = json.dumps(key_obj, sort_keys=True, ensure_ascii=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def stats(self) -> CacheStats:
        """Return current cache statistics."""
        self._stats.entries = len(self._data)
        return self._stats

    def clear(self) -> None:
        """Delete all cached entries and reset stats."""
        self._data.clear()
        self._stats = CacheStats()
        if self._path.exists():
            self._path.unlink()

    def invalidate(self, key: str) -> bool:
        """Remove a single entry. Returns True if it existed."""
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        s = self._stats
        return (
            f"ResponseCache(entries={len(self._data)}, "
            f"hits={s.hits}, misses={s.misses}, "
            f"cost_saved=${s.cost_saved_usd:.4f})"
        )

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            with open(self._path) as f:
                raw = json.load(f)
            for key, val in raw.items():
                self._data[key] = CacheEntry.from_dict(val)
        except (json.JSONDecodeError, KeyError):
            pass  # corrupt cache — start fresh

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(
                {k: v.to_dict() for k, v in self._data.items()},
                f,
                separators=(",", ":"),
            )
        tmp.replace(self._path)
