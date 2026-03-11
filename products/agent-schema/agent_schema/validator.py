"""
SchemaValidator — validates dicts against a simplified JSON Schema subset.
Zero external dependencies.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ValidationResult:
    valid: bool
    errors: list
    data: Optional[dict] = None


class SchemaValidator:
    """Validates a dict/str against a simple JSON schema. Zero deps."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate(self, data: Any, schema: dict) -> ValidationResult:
        """Validate an already-parsed Python object against *schema*."""
        errors: list[str] = []
        self._validate_node(data, schema, path="root", errors=errors)
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            data=data if len(errors) == 0 else None,
        )

    def parse_and_validate(self, text: str, schema: dict) -> ValidationResult:
        """
        Parse *text* as JSON (including text embedded in markdown code fences),
        then validate the parsed object.
        """
        from .extractor import JSONExtractor

        extractor = JSONExtractor()
        parsed = extractor.extract_and_parse(text)

        if parsed is None:
            return ValidationResult(
                valid=False,
                errors=["Could not parse JSON from input text"],
                data=None,
            )

        return self.validate(parsed, schema)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_node(
        self, value: Any, schema: dict, path: str, errors: list[str]
    ) -> None:
        if not isinstance(schema, dict):
            return

        expected_type = schema.get("type")
        if expected_type is not None:
            if not self._check_type(value, expected_type):
                errors.append(
                    f"{path}: expected type '{expected_type}', "
                    f"got '{self._type_name(value)}'"
                )
                # No point checking constraints if the type is already wrong.
                return

        # --- enum ---
        if "enum" in schema:
            if value not in schema["enum"]:
                errors.append(
                    f"{path}: value {value!r} not in enum {schema['enum']!r}"
                )

        # --- number / integer constraints ---
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in schema and value < schema["minimum"]:
                errors.append(
                    f"{path}: {value} is less than minimum {schema['minimum']}"
                )
            if "maximum" in schema and value > schema["maximum"]:
                errors.append(
                    f"{path}: {value} is greater than maximum {schema['maximum']}"
                )

        # --- string constraints ---
        if isinstance(value, str):
            if "minLength" in schema and len(value) < schema["minLength"]:
                errors.append(
                    f"{path}: string length {len(value)} is less than "
                    f"minLength {schema['minLength']}"
                )
            if "maxLength" in schema and len(value) > schema["maxLength"]:
                errors.append(
                    f"{path}: string length {len(value)} is greater than "
                    f"maxLength {schema['maxLength']}"
                )

        # --- array constraints ---
        if isinstance(value, list):
            items_schema = schema.get("items")
            if items_schema:
                for i, item in enumerate(value):
                    self._validate_node(
                        item, items_schema, path=f"{path}[{i}]", errors=errors
                    )

        # --- object constraints ---
        if isinstance(value, dict):
            # required fields
            for req in schema.get("required", []):
                if req not in value:
                    errors.append(f"{path}: missing required field '{req}'")

            # properties
            props = schema.get("properties", {})
            for prop_name, prop_schema in props.items():
                if prop_name in value:
                    self._validate_node(
                        value[prop_name],
                        prop_schema,
                        path=f"{path}.{prop_name}",
                        errors=errors,
                    )

    # ------------------------------------------------------------------
    # Type checking helpers
    # ------------------------------------------------------------------

    _TYPE_CHECKS = {
        "string": lambda v: isinstance(v, str),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "boolean": lambda v: isinstance(v, bool),
        "array": lambda v: isinstance(v, list),
        "object": lambda v: isinstance(v, dict),
        "null": lambda v: v is None,
    }

    def _check_type(self, value: Any, type_name: str) -> bool:
        checker = self._TYPE_CHECKS.get(type_name)
        if checker is None:
            # Unknown type — pass through
            return True
        return checker(value)

    @staticmethod
    def _type_name(value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, int):
            return "integer"
        if isinstance(value, float):
            return "number"
        if isinstance(value, str):
            return "string"
        if isinstance(value, list):
            return "array"
        if isinstance(value, dict):
            return "object"
        return type(value).__name__
