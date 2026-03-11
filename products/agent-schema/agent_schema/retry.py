"""
RetrySchema — wraps an LLM client to auto-retry until the response matches a schema.
Zero external dependencies.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, List, Optional

from .extractor import JSONExtractor
from .validator import SchemaValidator


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class SchemaValidationError(Exception):
    """Raised when LLM response fails schema validation (single attempt)."""

    def __init__(self, errors: list, response: str) -> None:
        self.errors = errors
        self.response = response
        super().__init__(
            f"Schema validation failed: {'; '.join(errors)}"
        )


class SchemaMaxRetriesExceeded(Exception):
    """Raised when all retry attempts are exhausted without a valid response."""

    def __init__(self, attempts: int, last_errors: list) -> None:
        self.attempts = attempts
        self.last_errors = last_errors
        super().__init__(
            f"Max retries ({attempts}) exceeded. "
            f"Last errors: {'; '.join(last_errors)}"
        )


# ---------------------------------------------------------------------------
# RetrySchema
# ---------------------------------------------------------------------------


class RetrySchema:
    """Wraps an LLM client to auto-retry until response matches schema."""

    _RETRY_USER_MESSAGE = (
        "Your response had validation errors: {errors}. "
        "Please fix and respond with valid JSON only."
    )

    def __init__(self, client: Any, model: str, max_retries: int = 3) -> None:
        self.client = client
        self.model = model
        self.max_retries = max_retries
        self._extractor = JSONExtractor()
        self._validator = SchemaValidator()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def complete(
        self,
        messages: list,
        schema: dict,
        system: Optional[str] = None,
    ) -> dict:
        """
        Call LLM, validate response against schema, retry with error feedback if invalid.

        On failure appends to messages:
          - assistant: <invalid response>
          - user: "Your response had validation errors: …"

        Raises SchemaMaxRetriesExceeded if all retries fail.
        Returns validated dict on success.
        """
        msgs = list(messages)  # shallow copy so caller's list is not mutated
        last_errors: list[str] = []

        for attempt in range(1, self.max_retries + 1):
            raw = self._call_sync(msgs, system)
            result = self._validator.parse_and_validate(raw, schema)

            if result.valid:
                return result.data  # type: ignore[return-value]

            last_errors = result.errors

            # Append the assistant's bad response + correction prompt
            msgs.append({"role": "assistant", "content": raw})
            msgs.append({
                "role": "user",
                "content": self._RETRY_USER_MESSAGE.format(
                    errors="; ".join(last_errors)
                ),
            })

        raise SchemaMaxRetriesExceeded(
            attempts=self.max_retries,
            last_errors=last_errors,
        )

    async def acomplete(
        self,
        messages: list,
        schema: dict,
        system: Optional[str] = None,
    ) -> dict:
        """Async version of complete()."""
        msgs = list(messages)
        last_errors: list[str] = []

        for attempt in range(1, self.max_retries + 1):
            raw = await self._call_async(msgs, system)
            result = self._validator.parse_and_validate(raw, schema)

            if result.valid:
                return result.data  # type: ignore[return-value]

            last_errors = result.errors

            msgs.append({"role": "assistant", "content": raw})
            msgs.append({
                "role": "user",
                "content": self._RETRY_USER_MESSAGE.format(
                    errors="; ".join(last_errors)
                ),
            })

        raise SchemaMaxRetriesExceeded(
            attempts=self.max_retries,
            last_errors=last_errors,
        )

    # ------------------------------------------------------------------
    # Client detection + dispatch
    # ------------------------------------------------------------------

    def _is_anthropic(self) -> bool:
        return hasattr(self.client, "messages")

    def _is_openai(self) -> bool:
        return hasattr(self.client, "chat")

    def _call_sync(self, messages: list, system: Optional[str]) -> str:
        if self._is_anthropic():
            return self._anthropic_call(messages, system)
        if self._is_openai():
            return self._openai_call(messages, system)
        raise ValueError(
            "Unsupported client. Expected Anthropic (has .messages) "
            "or OpenAI (has .chat) client."
        )

    async def _call_async(self, messages: list, system: Optional[str]) -> str:
        if self._is_anthropic():
            return await self._anthropic_acall(messages, system)
        if self._is_openai():
            return await self._openai_acall(messages, system)
        raise ValueError(
            "Unsupported client. Expected Anthropic (has .messages) "
            "or OpenAI (has .chat) client."
        )

    # ------------------------------------------------------------------
    # Anthropic
    # ------------------------------------------------------------------

    def _anthropic_call(self, messages: list, system: Optional[str]) -> str:
        kwargs: dict = dict(
            model=self.model,
            messages=messages,
            max_tokens=1024,
        )
        if system:
            kwargs["system"] = system
        response = self.client.messages.create(**kwargs)
        return self._anthropic_text(response)

    async def _anthropic_acall(self, messages: list, system: Optional[str]) -> str:
        kwargs: dict = dict(
            model=self.model,
            messages=messages,
            max_tokens=1024,
        )
        if system:
            kwargs["system"] = system
        response = await self.client.messages.create(**kwargs)
        return self._anthropic_text(response)

    @staticmethod
    def _anthropic_text(response: Any) -> str:
        # response.content is a list of content blocks
        blocks = response.content
        for block in blocks:
            if hasattr(block, "text"):
                return block.text
        return str(blocks)

    # ------------------------------------------------------------------
    # OpenAI
    # ------------------------------------------------------------------

    def _openai_call(self, messages: list, system: Optional[str]) -> str:
        msgs = self._inject_system_openai(messages, system)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=msgs,
        )
        return self._openai_text(response)

    async def _openai_acall(self, messages: list, system: Optional[str]) -> str:
        msgs = self._inject_system_openai(messages, system)
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=msgs,
        )
        return self._openai_text(response)

    @staticmethod
    def _inject_system_openai(messages: list, system: Optional[str]) -> list:
        if not system:
            return messages
        # Prepend a system message if caller did not already include one
        if messages and messages[0].get("role") == "system":
            return messages
        return [{"role": "system", "content": system}] + list(messages)

    @staticmethod
    def _openai_text(response: Any) -> str:
        return response.choices[0].message.content
