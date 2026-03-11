"""
agent-stream: Streaming LLM response handling for AI agents.
Collect chunks, track tokens, handle cancellation. Works with Anthropic and OpenAI.
"""

from .collector import StreamCollector, StreamResult, StreamError
from .async_collector import AsyncStreamCollector

__all__ = [
    "StreamCollector",
    "StreamResult",
    "StreamError",
    "AsyncStreamCollector",
]

__version__ = "0.1.0"
