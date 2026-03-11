"""
Auto-redact sensitive patterns from log values before emission.
Only string values are redacted — keys are never modified.
"""

import re
from typing import Any, Dict

# Patterns that indicate a secret in an env-var-style key name
_SECRET_KEY_PATTERNS = re.compile(
    r"(SECRET|TOKEN|KEY|PASSWORD)", re.IGNORECASE
)

# Value patterns to redact
_VALUE_PATTERNS = [
    # Anthropic / OpenAI API keys
    (re.compile(r"sk-[a-zA-Z0-9]{32,}"), "[REDACTED:api_key]"),
    # GitHub personal access tokens
    (re.compile(r"ghp_[a-zA-Z0-9]+"), "[REDACTED:gh_token]"),
    # Authorization headers
    (re.compile(r"Bearer [a-zA-Z0-9._\-]+"), "Bearer [REDACTED]"),
]


def redact_string(value: str) -> str:
    """Apply all value-level redaction patterns to a single string."""
    for pattern, replacement in _VALUE_PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def redact_value(key: str, value: Any) -> Any:
    """
    Redact a value based on its key name and content.
    Returns the redacted value (or the original if no redaction needed).
    """
    if isinstance(value, str):
        # If the key looks like a secret field, blank the whole value
        if _SECRET_KEY_PATTERNS.search(key):
            return "[REDACTED]"
        return redact_string(value)
    return value


def redact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively redact all string values in a dict.
    Keys are never modified.
    """
    result: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = redact_dict(value)
        elif isinstance(value, list):
            result[key] = [
                redact_dict(item) if isinstance(item, dict)
                else redact_value(key, item) if isinstance(item, str)
                else item
                for item in value
            ]
        else:
            result[key] = redact_value(key, value)
    return result
