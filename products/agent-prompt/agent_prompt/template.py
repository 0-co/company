"""
PromptTemplate and ChatTemplate — core template classes.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _render(text: str, variables: Dict[str, Any]) -> str:
    """
    Render a template string with {variable} placeholders.
    Supports literal brace escaping: {{ → { and }} → }.
    Raises KeyError if a required variable is missing.
    """
    # Single-brace variables: {var} but not {{var}} or {var}}
    # Match {identifier} that is NOT preceded or followed by another brace.
    _VAR_RE = re.compile(r"(?<!\{)\{([A-Za-z_][A-Za-z0-9_]*)\}(?!\})")

    required = set(_VAR_RE.findall(text))

    # Check for missing variables
    missing = required - set(variables.keys())
    if missing:
        raise KeyError(
            f"Missing template variables: {sorted(missing)}. "
            f"Provided: {sorted(variables.keys())}"
        )

    # Replace {var} with values
    def _sub(m: re.Match) -> str:
        return str(variables[m.group(1)])

    result = _VAR_RE.sub(_sub, text)
    # Unescape {{ → { and }} → }
    result = result.replace("{{", "{").replace("}}", "}")
    return result


class PromptTemplate:
    """
    A single-message prompt template with {variable} placeholder syntax.

    Example::

        from agent_prompt import PromptTemplate

        tmpl = PromptTemplate(
            "You are a {role}. Answer the user's question: {question}"
        )

        text = tmpl.render(role="Python expert", question="What is a decorator?")
        msg  = tmpl.to_message("user", role="Python expert", question="What is a decorator?")
        # {"role": "user", "content": "You are a Python expert. Answer..."}

    Escape literal braces with doubling: {{this stays as-is}}.
    """

    def __init__(self, template: str):
        self.template = template
        self._variables: Optional[List[str]] = None

    @property
    def variables(self) -> List[str]:
        """Variable names required by this template (sorted, deduplicated)."""
        if self._variables is None:
            _VAR_RE = re.compile(r"(?<!\{)\{([A-Za-z_][A-Za-z0-9_]*)\}(?!\})")
            self._variables = sorted(set(_VAR_RE.findall(self.template)))
        return self._variables

    def render(self, **kwargs: Any) -> str:
        """
        Render the template with the given keyword arguments.
        Raises KeyError if any required variable is missing.
        """
        return _render(self.template, kwargs)

    def partial(self, **kwargs: Any) -> "PromptTemplate":
        """
        Return a new PromptTemplate with some variables pre-filled.
        Remaining {variables} stay as-is.

        Example::

            base = PromptTemplate("Hello {name}, you are {role}")
            for_user = base.partial(name="Alice")
            text = for_user.render(role="assistant")
        """
        filled = self.template
        for key, value in kwargs.items():
            filled = filled.replace("{" + key + "}", str(value))
        return PromptTemplate(filled)

    def to_message(self, msg_role: str, **kwargs: Any) -> Dict[str, str]:
        """
        Render and return as a message dict: {"role": msg_role, "content": rendered}.
        Compatible with Anthropic and OpenAI message formats.
        Note: uses ``msg_role`` as the parameter name to avoid collision with
        templates that have a ``{role}`` variable.
        """
        return {"role": msg_role, "content": self.render(**kwargs)}

    def estimate_tokens(self, **kwargs: Any) -> int:
        """
        Estimate token count of the rendered text.
        Uses character-based heuristic (~4 chars per token). Good to ±20%.
        """
        from .estimate import estimate_tokens
        return estimate_tokens(self.render(**kwargs))

    def __add__(self, other: "PromptTemplate") -> "PromptTemplate":
        """Concatenate two templates. Variables are unioned."""
        return PromptTemplate(self.template + other.template)

    def __repr__(self) -> str:
        preview = self.template[:60] + ("..." if len(self.template) > 60 else "")
        return f"PromptTemplate({preview!r}, vars={self.variables})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PromptTemplate) and self.template == other.template


@dataclass
class Message:
    """
    A rendered (or template) message in a chat conversation.
    Role is one of: "system", "user", "assistant".

    Can be created from a PromptTemplate::

        msg = Message.from_template("system", PromptTemplate("You are a {role}"), role="assistant")
    """

    role: str
    content: str

    @classmethod
    def from_template(cls, role: str, template: PromptTemplate, **kwargs: Any) -> "Message":
        return cls(role=role, content=template.render(**kwargs))

    def to_dict(self) -> Dict[str, str]:
        """Return {"role": ..., "content": ...} compatible with Anthropic/OpenAI."""
        return {"role": self.role, "content": self.content}

    def estimate_tokens(self) -> int:
        from .estimate import estimate_tokens
        return estimate_tokens(self.content)


class ChatTemplate:
    """
    A multi-turn conversation template.
    Compose system prompt + user/assistant turns, render all at once.

    Example::

        from agent_prompt import ChatTemplate, PromptTemplate

        chat = ChatTemplate(
            system=PromptTemplate("You are a helpful {language} assistant."),
            turns=[
                ("user",      PromptTemplate("Explain {concept} briefly.")),
                ("assistant", PromptTemplate("Sure! {concept} is...")),
                ("user",      PromptTemplate("Give an example.")),
            ]
        )

        messages = chat.render(language="Python", concept="decorators")
        # [
        #   {"role": "system",    "content": "You are a helpful Python assistant."},
        #   {"role": "user",      "content": "Explain decorators briefly."},
        #   {"role": "assistant", "content": "Sure! decorators is..."},
        #   {"role": "user",      "content": "Give an example."},
        # ]

        # Render only the turns (no system message):
        messages = chat.render_turns(language="Python", concept="decorators")
    """

    def __init__(
        self,
        system: Optional[PromptTemplate] = None,
        turns: Optional[List[tuple]] = None,
    ):
        """
        Parameters
        ----------
        system:
            Optional system prompt template.
        turns:
            List of (role, PromptTemplate) tuples defining the conversation.
        """
        self.system = system
        self.turns: List[tuple] = turns or []

    def add_turn(self, role: str, template: PromptTemplate) -> "ChatTemplate":
        """Append a turn and return self for chaining."""
        self.turns.append((role, template))
        return self

    @property
    def variables(self) -> List[str]:
        """All unique variables required across system + turns."""
        names = set()
        if self.system:
            names.update(self.system.variables)
        for _, tmpl in self.turns:
            names.update(tmpl.variables)
        return sorted(names)

    def render(self, **kwargs: Any) -> List[Dict[str, str]]:
        """
        Render all messages (system + turns) with shared variables.
        Returns list of {"role": ..., "content": ...} dicts.
        """
        messages: List[Dict[str, str]] = []

        if self.system:
            messages.append({"role": "system", "content": self.system.render(**kwargs)})

        for role, tmpl in self.turns:
            messages.append({"role": role, "content": tmpl.render(**kwargs)})

        return messages

    def render_turns(self, **kwargs: Any) -> List[Dict[str, str]]:
        """Render only the conversation turns, no system message."""
        return [
            {"role": role, "content": tmpl.render(**kwargs)}
            for role, tmpl in self.turns
        ]

    def estimate_tokens(self, **kwargs: Any) -> int:
        """Estimate total token count for all messages combined."""
        from .estimate import estimate_tokens
        total = 0
        for msg in self.render(**kwargs):
            total += estimate_tokens(msg["content"])
        return total

    def partial(self, **kwargs: Any) -> "ChatTemplate":
        """
        Pre-fill some variables, return a new ChatTemplate with remaining
        {placeholders} intact.
        """
        new_system = self.system.partial(**kwargs) if self.system else None
        new_turns = [(role, tmpl.partial(**kwargs)) for role, tmpl in self.turns]
        return ChatTemplate(system=new_system, turns=new_turns)

    def __repr__(self) -> str:
        n_turns = len(self.turns)
        has_sys = self.system is not None
        return f"ChatTemplate(system={has_sys}, turns={n_turns}, vars={self.variables})"
