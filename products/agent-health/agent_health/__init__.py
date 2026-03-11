"""
agent-health: Health checks for AI APIs.
Know before your agents do.
"""

from .checker import HealthChecker, HealthResult, HealthStatus
from .pool import HealthPool
from .probe import Probe, AnthropicProbe, OpenAIProbe, CustomProbe

__all__ = [
    "HealthChecker",
    "HealthResult",
    "HealthStatus",
    "HealthPool",
    "Probe",
    "AnthropicProbe",
    "OpenAIProbe",
    "CustomProbe",
]

__version__ = "0.1.0"
