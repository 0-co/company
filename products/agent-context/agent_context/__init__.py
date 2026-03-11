"""agent-context — prevent context rot in long-running AI agents."""

from .context import ContextManager, ContextOverflow, trim

__all__ = ["ContextManager", "ContextOverflow", "trim"]
__version__ = "0.1.0"
