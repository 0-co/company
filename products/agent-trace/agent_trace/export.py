"""Export helpers — format and write completed spans."""

import json
from typing import Any, Dict, List


def spans_to_jsonl(spans: List[Dict[str, Any]]) -> str:
    """Serialize a list of span dicts to a JSONL string (one span per line)."""
    lines = [json.dumps(span) for span in spans]
    return "\n".join(lines) + ("\n" if lines else "")


def write_jsonl(path: str, spans: List[Dict[str, Any]], append: bool = True) -> None:
    """Write spans to a JSONL file.

    append=True (default) adds to an existing file. append=False overwrites it.
    """
    mode = "a" if append else "w"
    with open(path, mode, encoding="utf-8") as fh:
        for span in spans:
            fh.write(json.dumps(span) + "\n")


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    """Read spans back from a JSONL file."""
    spans: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                spans.append(json.loads(line))
    return spans
