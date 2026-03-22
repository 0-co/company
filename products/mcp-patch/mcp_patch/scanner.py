"""AST-based scanner core for mcp-patch."""

import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Finding:
    file: str
    line: int
    check: str
    severity: str  # CRITICAL, HIGH, MEDIUM
    description: str
    snippet: str
    fix: str
    param: str = ""


def scan_file(path: str) -> list[Finding]:
    """Parse a Python file and return all security findings."""
    source_path = Path(path)
    try:
        source = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Cannot read {path}: {exc}") from exc

    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as exc:
        raise RuntimeError(f"Syntax error in {path}: {exc}") from exc

    source_lines = source.splitlines()
    findings: list[Finding] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        if not _is_tool_function(node):
            continue

        params = _collect_params(node)
        if not params:
            continue

        from mcp_patch.checks import run_all_checks
        findings.extend(run_all_checks(node, params, source_lines, path))

    return findings


def _is_tool_function(node: ast.FunctionDef) -> bool:
    """Return True if this function has a @tool or @mcp.tool() decorator."""
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == "tool":
            return True
        # @mcp.tool or @mcp.tool()
        if isinstance(decorator, ast.Attribute) and decorator.attr == "tool":
            return True
        if isinstance(decorator, ast.Call):
            func = decorator.func
            if isinstance(func, ast.Name) and func.id == "tool":
                return True
            if isinstance(func, ast.Attribute) and func.attr == "tool":
                return True
    return False


def _collect_params(node: ast.FunctionDef) -> set[str]:
    """Collect all non-self parameter names from a function definition."""
    params: set[str] = set()
    for arg in node.args.args:
        if arg.arg not in ("self", "cls"):
            params.add(arg.arg)
    for arg in node.args.kwonlyargs:
        params.add(arg.arg)
    if node.args.vararg:
        params.add(node.args.vararg.arg)
    if node.args.kwarg:
        params.add(node.args.kwarg.arg)
    return params


def get_snippet(source_lines: list[str], lineno: int) -> str:
    """Return the source line at lineno (1-indexed), stripped."""
    if 1 <= lineno <= len(source_lines):
        return source_lines[lineno - 1].strip()
    return ""
