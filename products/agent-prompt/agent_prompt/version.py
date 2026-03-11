"""
PromptVersion: label and hash prompt templates for tracking and A/B testing.
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .template import PromptTemplate, ChatTemplate


@dataclass
class PromptVersion:
    """
    A versioned prompt template.

    Tracks: label, content hash, creation timestamp, and optional metadata.
    Useful for:
    - Pinning a specific prompt version in production
    - A/B testing different prompts
    - Auditing which prompt version generated a result

    Example::

        from agent_prompt import PromptTemplate, PromptVersion

        tmpl = PromptTemplate("You are a {role}. Answer: {question}")
        v1 = PromptVersion(tmpl, label="v1.0", metadata={"author": "eng"})

        print(v1.hash)     # sha256 prefix of template content
        print(v1.label)    # "v1.0"
        print(v1.created_at)  # Unix timestamp

        # Use as normal template
        result = v1.render(role="expert", question="What is entropy?")

    Compare versions::

        v2 = PromptVersion(updated_tmpl, label="v1.1")
        if v1.hash != v2.hash:
            print("Prompt changed!")
    """

    template: Any  # PromptTemplate or ChatTemplate
    label: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def __post_init__(self):
        if isinstance(self.template, PromptTemplate):
            self._content = self.template.template
        elif isinstance(self.template, ChatTemplate):
            parts = []
            if self.template.system:
                parts.append(("system", self.template.system.template))
            for role, tmpl in self.template.turns:
                parts.append((role, tmpl.template))
            self._content = json.dumps(parts)
        else:
            self._content = str(self.template)

    @property
    def hash(self) -> str:
        """SHA-256 hex digest (first 12 chars) of the template content."""
        return hashlib.sha256(self._content.encode()).hexdigest()[:12]

    def render(self, **kwargs: Any) -> Any:
        """Delegate to the underlying template's render method."""
        return self.template.render(**kwargs)

    def to_message(self, msg_role: str, **kwargs: Any) -> Dict[str, str]:
        """Delegate to PromptTemplate.to_message (raises if ChatTemplate)."""
        if not isinstance(self.template, PromptTemplate):
            raise TypeError("to_message() only works with PromptTemplate, not ChatTemplate")
        return self.template.to_message(msg_role, **kwargs)

    def __eq__(self, other: object) -> bool:
        """Two PromptVersions are equal if their content hashes match."""
        return isinstance(other, PromptVersion) and self.hash == other.hash

    def __repr__(self) -> str:
        label = f" label={self.label!r}" if self.label else ""
        return f"PromptVersion(hash={self.hash!r}{label})"
