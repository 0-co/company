"""
agent-log — structured logging for AI agents.

Zero dependencies, Python 3.8+.

Quick start:
    from agent_log import AgentLogger

    log = AgentLogger("my-agent")
    with log.session(task="summarize docs") as session:
        session.info("Starting")
        with session.span("llm_call", model="claude-opus-4") as span:
            span.tokens(prompt=500, completion=100, model="claude-opus-4")
        session.tool_call("read_file", args={"path": "/tmp/data.txt"}, result_summary="3.2KB")
        session.decision("Will summarize with the LLM")
"""

from .logger import AgentLogger
from .session import Session
from .span import Span, TOKEN_COSTS
from .redactor import redact_string, redact_dict

__all__ = [
    "AgentLogger",
    "Session",
    "Span",
    "TOKEN_COSTS",
    "redact_string",
    "redact_dict",
]

__version__ = "0.1.0"
