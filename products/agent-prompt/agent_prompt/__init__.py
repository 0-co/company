"""
agent-prompt: Prompt templates for AI agents.
LangChain has prompt templates. You don't need LangChain.
"""

from .template import PromptTemplate, ChatTemplate, Message
from .version import PromptVersion
from .estimate import estimate_tokens

__all__ = [
    "PromptTemplate",
    "ChatTemplate",
    "Message",
    "PromptVersion",
    "estimate_tokens",
]

__version__ = "0.1.0"
