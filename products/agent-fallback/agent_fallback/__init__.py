"""agent-fallback — zero-dep multi-provider failover for AI agents."""

from .fallback import Fallback, Provider, FallbackResult, ProviderFailed
from .circuit import CircuitBreaker, CircuitOpen

__version__ = "0.1.0"
__all__ = [
    "Fallback",
    "Provider",
    "FallbackResult",
    "ProviderFailed",
    "CircuitBreaker",
    "CircuitOpen",
]
