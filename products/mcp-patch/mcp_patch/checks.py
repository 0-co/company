"""Security checks for MCP tool functions.

Each check_* function receives:
    node        - ast.FunctionDef of the @tool function
    params      - set of parameter names
    source_lines - list of source code lines (0-indexed by line - 1)
    path        - source file path string

Each returns a list of Finding objects (may be empty).
"""

import ast
from typing import Callable

from mcp_patch.scanner import Finding, get_snippet


# ---------------------------------------------------------------------------
# Helper: name extraction
# ---------------------------------------------------------------------------

def _names_in_node(node: ast.AST) -> set[str]:
    """Recursively collect all Name ids referenced inside an AST node."""
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            names.add(child.id)
    return names


def _fstring_references_param(node: ast.JoinedStr, params: set[str]) -> bool:
    """Return True if an f-string interpolates any tool parameter."""
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and child.id in params:
            return True
    return False


def _format_call_references_param(node: ast.Call, params: set[str]) -> bool:
    """Return True if a .format() call includes a tool parameter."""
    for arg in node.args:
        if _names_in_node(arg) & params:
            return True
    for keyword in node.keywords:
        if _names_in_node(keyword.value) & params:
            return True
    return False


def _arg_references_param(arg_node: ast.AST, params: set[str]) -> bool:
    """Return True if an argument node directly or transitively references a param."""
    # Direct Name reference
    if isinstance(arg_node, ast.Name) and arg_node.id in params:
        return True
    # f-string interpolation
    if isinstance(arg_node, ast.JoinedStr):
        return _fstring_references_param(arg_node, params)
    # "template".format(param) or template.format(param)
    if (
        isinstance(arg_node, ast.Call)
        and isinstance(arg_node.func, ast.Attribute)
        and arg_node.func.attr == "format"
    ):
        return _format_call_references_param(arg_node, params)
    # %-formatting: "cmd %s" % param  (BinOp with Mod)
    if isinstance(arg_node, ast.BinOp) and isinstance(arg_node.op, ast.Mod):
        return bool(_names_in_node(arg_node.right) & params)
    # Concatenation: "prefix" + param
    if isinstance(arg_node, ast.BinOp) and isinstance(arg_node.op, ast.Add):
        return bool(_names_in_node(arg_node) & params)
    return False


# ---------------------------------------------------------------------------
# Check 1: shell_injection
# ---------------------------------------------------------------------------

# subprocess functions that matter
_SUBPROCESS_FUNCS = {"run", "Popen", "call", "check_call", "check_output"}
# single-argument shell APIs
_OS_SHELL_FUNCS = {"system", "popen"}


def _is_shell_true(call_node: ast.Call) -> bool:
    """Return True if the call has shell=True keyword argument."""
    for kw in call_node.keywords:
        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
            return True
    return False


def _first_arg(call_node: ast.Call) -> ast.AST | None:
    if call_node.args:
        return call_node.args[0]
    for kw in call_node.keywords:
        if kw.arg in ("args", "cmd", "command"):
            return kw.value
    return None


def check_shell_injection(
    node: ast.FunctionDef,
    params: set[str],
    source_lines: list[str],
    path: str,
) -> list[Finding]:
    findings: list[Finding] = []

    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue

        func = child.func

        # subprocess.run/Popen/call/etc with shell=True
        if (
            isinstance(func, ast.Attribute)
            and func.attr in _SUBPROCESS_FUNCS
            and isinstance(func.value, ast.Name)
            and func.value.id == "subprocess"
        ):
            if _is_shell_true(child):
                first = _first_arg(child)
                if first is not None and _arg_references_param(first, params):
                    param_hit = _names_in_node(first) & params
                    param_name = next(iter(param_hit))
                    findings.append(Finding(
                        file=path,
                        line=child.lineno,
                        check="shell_injection",
                        severity="CRITICAL",
                        description=(
                            f"subprocess.{func.attr}(..., shell=True) — "
                            f"tool param '{param_name}' flows to shell"
                        ),
                        snippet=get_snippet(source_lines, child.lineno),
                        fix="Use subprocess.run([cmd, shlex.quote(arg)]) without shell=True",
                        param=param_name,
                    ))

        # os.system(f"...{param}...") or os.popen(...)
        if (
            isinstance(func, ast.Attribute)
            and func.attr in _OS_SHELL_FUNCS
            and isinstance(func.value, ast.Name)
            and func.value.id == "os"
        ):
            first = _first_arg(child)
            if first is not None and _arg_references_param(first, params):
                param_hit = _names_in_node(first) & params
                param_name = next(iter(param_hit))
                findings.append(Finding(
                    file=path,
                    line=child.lineno,
                    check="shell_injection",
                    severity="CRITICAL",
                    description=(
                        f"os.{func.attr}() — "
                        f"tool param '{param_name}' flows to shell"
                    ),
                    snippet=get_snippet(source_lines, child.lineno),
                    fix="Use subprocess.run([...], shell=False) instead of os.system/os.popen",
                    param=param_name,
                ))

    return findings


# ---------------------------------------------------------------------------
# Check 2: path_traversal
# ---------------------------------------------------------------------------

# Attribute access on a Path object that extracts only the filename component — safe.
# e.g., Path(user_input).name is safe; Path(user_input).read_text() is not.
_SAFE_PATH_ATTRS = {"name", "stem", "suffix", "suffixes", "parts"}


def _call_node_is_safely_chained(call_node: ast.Call, tree_root: ast.AST) -> bool:
    """Return True if Path(param) is immediately chained with a safe attribute (name/stem/suffix).

    Path(param).name extracts only the filename — safe to use with a base directory check.
    Path(param).read_text() still reads from an arbitrary path — not safe.
    """
    for parent in ast.walk(tree_root):
        if (
            isinstance(parent, ast.Attribute)
            and parent.value is call_node
            and parent.attr in _SAFE_PATH_ATTRS
        ):
            return True
    return False


def check_path_traversal(
    node: ast.FunctionDef,
    params: set[str],
    source_lines: list[str],
    path: str,
) -> list[Finding]:
    findings: list[Finding] = []

    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue

        func = child.func
        call_name: str | None = None

        # open(param, ...)
        if isinstance(func, ast.Name) and func.id == "open":
            call_name = "open"

        # pathlib.Path(param) or Path(param)
        if isinstance(func, ast.Attribute) and func.attr == "Path":
            call_name = "Path"
        if isinstance(func, ast.Name) and func.id == "Path":
            call_name = "Path"

        if call_name is None:
            continue

        first = _first_arg(child)
        if first is None:
            continue

        # Only flag direct Name reference (param used as-is), not f-strings
        # (f-strings could be constructing safe paths)
        if not (isinstance(first, ast.Name) and first.id in params):
            continue

        param_name = first.id

        # Path(param).name or Path(param).stem — these extract only the filename component,
        # which is safe when combined with a base directory join. Skip those cases.
        # Path(param).read_text() or Path(param).open() still reads the full path — flag it.
        if call_name == "Path" and _call_node_is_safely_chained(child, node):
            continue

        findings.append(Finding(
            file=path,
            line=child.lineno,
            check="path_traversal",
            severity="HIGH",
            description=(
                f"{call_name}({param_name}) — "
                f"tool param '{param_name}' used as file path without validation"
            ),
            snippet=get_snippet(source_lines, child.lineno),
            fix=(
                "Use (base_dir / Path(filename).name).resolve() "
                "and verify result starts with base_dir"
            ),
            param=param_name,
        ))

    return findings


# ---------------------------------------------------------------------------
# Check 3: ssrf
# ---------------------------------------------------------------------------

# HTTP client functions that accept a URL as first positional argument
_HTTP_METHODS = {"get", "post", "put", "delete", "patch", "head", "options", "request"}
# Known HTTP client library names
_HTTP_LIBS = {"requests", "httpx", "urllib"}


def _is_url_open(call_node: ast.Call, func: ast.AST) -> bool:
    """Return True if this is urllib.request.urlopen(...)."""
    # urllib.request.urlopen
    if (
        isinstance(func, ast.Attribute)
        and func.attr == "urlopen"
        and isinstance(func.value, ast.Attribute)
        and func.value.attr == "request"
        and isinstance(func.value.value, ast.Name)
        and func.value.value.id == "urllib"
    ):
        return True
    # urlopen directly imported
    if isinstance(func, ast.Name) and func.id == "urlopen":
        return True
    return False


def check_ssrf(
    node: ast.FunctionDef,
    params: set[str],
    source_lines: list[str],
    path: str,
) -> list[Finding]:
    findings: list[Finding] = []

    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue

        func = child.func
        call_label: str | None = None

        # requests.get(url), httpx.post(url), etc.
        if (
            isinstance(func, ast.Attribute)
            and func.attr in _HTTP_METHODS
            and isinstance(func.value, ast.Name)
            and func.value.id in _HTTP_LIBS
        ):
            call_label = f"{func.value.id}.{func.attr}"

        # urllib.request.urlopen(url)
        if _is_url_open(child, func):
            call_label = "urllib.request.urlopen"

        if call_label is None:
            continue

        # URL is typically the first positional argument
        first = _first_arg(child)
        if first is None:
            continue

        # Direct param reference or param used in f-string/concat for the URL
        if isinstance(first, ast.Name) and first.id in params:
            param_name = first.id
        elif isinstance(first, ast.JoinedStr) and _fstring_references_param(first, params):
            param_hit = _names_in_node(first) & params
            param_name = next(iter(param_hit))
        else:
            continue

        findings.append(Finding(
            file=path,
            line=child.lineno,
            check="ssrf",
            severity="HIGH",
            description=(
                f"{call_label}({param_name}) — "
                f"tool param '{param_name}' used as URL without validation"
            ),
            snippet=get_snippet(source_lines, child.lineno),
            fix=(
                "Validate URL scheme and host against an allowlist before making requests. "
                "Block private IP ranges (169.254.x.x, 10.x.x.x, 172.16-31.x.x, 192.168.x.x)."
            ),
            param=param_name,
        ))

    return findings


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_ALL_CHECKS: list[Callable] = [
    check_shell_injection,
    check_path_traversal,
    check_ssrf,
]


def run_all_checks(
    node: ast.FunctionDef,
    params: set[str],
    source_lines: list[str],
    path: str,
) -> list[Finding]:
    """Run every check against a single @tool function."""
    findings: list[Finding] = []
    for check_fn in _ALL_CHECKS:
        findings.extend(check_fn(node, params, source_lines, path))
    return findings
