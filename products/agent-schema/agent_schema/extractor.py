"""
JSONExtractor — pulls JSON out of messy LLM output.
Zero external dependencies.
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional, Union


class JSONExtractor:
    """Extracts JSON from messy LLM output (markdown code blocks, extra text, etc.)"""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, text: str) -> Optional[str]:
        """
        Try multiple strategies to find a JSON string inside *text*.

        Strategies (in order):
        1. Direct JSON parse of the entire text (stripped).
        2. Extract from ```json ... ``` fenced code block.
        3. Extract from ``` ... ``` fenced code block.
        4. Find first balanced { ... } block.
        5. Find first balanced [ ... ] block.

        Returns the raw JSON string, or None if nothing workable is found.
        """
        if not text:
            return None

        stripped = text.strip()

        # Strategy 1: whole text is already valid JSON
        candidate = self._try_parse(stripped)
        if candidate is not None:
            return stripped

        # Strategy 2: ```json ... ``` block
        result = self._extract_fenced(text, lang="json")
        if result is not None:
            return result

        # Strategy 3: ``` ... ``` block (no language tag)
        result = self._extract_fenced(text, lang="")
        if result is not None:
            return result

        # Strategy 4 & 5: find first balanced brace/bracket
        for opener, closer in [('{', '}'), ('[', ']')]:
            result = self._extract_balanced(text, opener, closer)
            if result is not None:
                return result

        return None

    def extract_and_parse(self, text: str) -> Optional[Union[dict, list]]:
        """
        Extract JSON string from *text* and parse it into a Python object.

        Returns the parsed dict/list, or None if extraction/parsing fails.
        """
        if text is None:
            return None

        raw = self.extract(text)
        if raw is None:
            return None

        return self._try_parse(raw)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _try_parse(text: str) -> Optional[Any]:
        """Return parsed JSON or None (never raises)."""
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return None

    @staticmethod
    def _extract_fenced(text: str, lang: str) -> Optional[str]:
        """
        Pull content out of a Markdown fenced code block.

        If *lang* is empty string, match blocks with no language tag.
        """
        if lang:
            pattern = r"```" + re.escape(lang) + r"\s*\n([\s\S]*?)```"
        else:
            # Match ``` with no tag (possibly whitespace-only before newline)
            pattern = r"```\s*\n([\s\S]*?)```"

        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            candidate = m.strip()
            parsed = JSONExtractor._try_parse(candidate)
            if parsed is not None:
                return candidate

        return None

    @staticmethod
    def _extract_balanced(text: str, opener: str, closer: str) -> Optional[str]:
        """
        Scan *text* for the first balanced block starting with *opener*
        and ending with the matching *closer*.

        Handles nested structures and quoted strings (to avoid counting
        braces/brackets inside string literals).
        """
        start = text.find(opener)
        if start == -1:
            return None

        depth = 0
        in_string = False
        escape_next = False
        i = start

        while i < len(text):
            ch = text[i]

            if escape_next:
                escape_next = False
                i += 1
                continue

            if ch == '\\' and in_string:
                escape_next = True
                i += 1
                continue

            if ch == '"':
                in_string = not in_string
                i += 1
                continue

            if in_string:
                i += 1
                continue

            if ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    candidate = text[start: i + 1]
                    parsed = JSONExtractor._try_parse(candidate)
                    if parsed is not None:
                        return candidate
                    # Balanced but not valid JSON — keep searching
                    next_start = text.find(opener, i + 1)
                    if next_start == -1:
                        return None
                    start = next_start
                    depth = 0
                    i = start
                    continue

            i += 1

        return None
