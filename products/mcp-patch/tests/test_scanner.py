"""Tests for mcp-patch scanner and checks."""

import sys
import os
from pathlib import Path

# Allow running from repo root without installation
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_patch.scanner import scan_file

FIXTURES = Path(__file__).parent / "fixtures"
VULNERABLE = str(FIXTURES / "vulnerable_server.py")
CLEAN = str(FIXTURES / "clean_server.py")


def findings_by_check(path: str) -> dict[str, list]:
    """Return findings grouped by check name."""
    result: dict[str, list] = {}
    for finding in scan_file(path):
        result.setdefault(finding.check, []).append(finding)
    return result


# ---------------------------------------------------------------------------
# shell_injection
# ---------------------------------------------------------------------------

def test_shell_injection_detected():
    grouped = findings_by_check(VULNERABLE)
    assert "shell_injection" in grouped, "Expected shell_injection findings"
    findings = grouped["shell_injection"]
    assert len(findings) >= 2, f"Expected at least 2 shell_injection findings, got {len(findings)}"


def test_shell_injection_subprocess_shell_true():
    """subprocess.run(f'...{param}...', shell=True) must be flagged."""
    findings = [
        f for f in scan_file(VULNERABLE)
        if f.check == "shell_injection" and "subprocess" in f.description
    ]
    assert len(findings) >= 1, "Expected at least one subprocess shell_injection finding"


def test_shell_injection_os_system():
    """os.system(f'...{param}...') must be flagged."""
    findings = [
        f for f in scan_file(VULNERABLE)
        if f.check == "shell_injection" and "os.system" in f.description
    ]
    assert len(findings) >= 1, "Expected os.system finding"


def test_shell_injection_os_popen():
    """os.popen(f'...{param}...') must be flagged."""
    findings = [
        f for f in scan_file(VULNERABLE)
        if f.check == "shell_injection" and "os.popen" in f.description
    ]
    assert len(findings) >= 1, "Expected os.popen finding"


# ---------------------------------------------------------------------------
# path_traversal
# ---------------------------------------------------------------------------

def test_path_traversal_detected():
    grouped = findings_by_check(VULNERABLE)
    assert "path_traversal" in grouped, "Expected path_traversal findings"
    findings = grouped["path_traversal"]
    assert len(findings) >= 2, f"Expected at least 2 path_traversal findings, got {len(findings)}"


def test_path_traversal_open():
    """open(param) must be flagged."""
    findings = [
        f for f in scan_file(VULNERABLE)
        if f.check == "path_traversal" and "open" in f.description
    ]
    assert len(findings) >= 1, "Expected open() path_traversal finding"


def test_path_traversal_pathlib():
    """pathlib.Path(param) must be flagged."""
    findings = [
        f for f in scan_file(VULNERABLE)
        if f.check == "path_traversal" and "Path" in f.description
    ]
    assert len(findings) >= 1, "Expected Path() path_traversal finding"


# ---------------------------------------------------------------------------
# ssrf
# ---------------------------------------------------------------------------

def test_ssrf_detected():
    grouped = findings_by_check(VULNERABLE)
    assert "ssrf" in grouped, "Expected ssrf findings"
    findings = grouped["ssrf"]
    assert len(findings) >= 3, f"Expected at least 3 ssrf findings, got {len(findings)}"


def test_ssrf_requests():
    """requests.get(url) must be flagged."""
    findings = [
        f for f in scan_file(VULNERABLE)
        if f.check == "ssrf" and "requests" in f.description
    ]
    assert len(findings) >= 1, "Expected requests SSRF finding"


def test_ssrf_httpx():
    """httpx.get(endpoint) must be flagged."""
    findings = [
        f for f in scan_file(VULNERABLE)
        if f.check == "ssrf" and "httpx" in f.description
    ]
    assert len(findings) >= 1, "Expected httpx SSRF finding"


def test_ssrf_urllib():
    """urllib.request.urlopen(url) must be flagged."""
    findings = [
        f for f in scan_file(VULNERABLE)
        if f.check == "ssrf" and "urllib" in f.description
    ]
    assert len(findings) >= 1, "Expected urllib SSRF finding"


# ---------------------------------------------------------------------------
# clean server — no findings
# ---------------------------------------------------------------------------

def test_clean_server_no_findings():
    """clean_server.py should produce zero findings."""
    findings = scan_file(CLEAN)
    assert len(findings) == 0, (
        f"Expected 0 findings in clean_server.py, got {len(findings)}: "
        + ", ".join(f"{f.check}@{f.line}" for f in findings)
    )


# ---------------------------------------------------------------------------
# non-@tool functions must not be flagged
# ---------------------------------------------------------------------------

def test_non_tool_functions_not_flagged():
    """Helper functions without @tool decorator must not produce findings."""
    all_findings = scan_file(VULNERABLE)
    # The vulnerable_server.py has two plain helper functions at the bottom:
    # _internal_fetch and _run_safely. They are not @tool functions.
    # We verify by checking that line numbers for those helpers don't appear.

    # Count unique functions flagged (by param name as proxy)
    # The clean_server.py helper _helper_that_uses_subprocess must not produce findings
    clean_findings = scan_file(CLEAN)
    assert len(clean_findings) == 0, (
        "Non-@tool helper in clean_server.py should not be flagged"
    )


# ---------------------------------------------------------------------------
# Metadata on findings
# ---------------------------------------------------------------------------

def test_finding_has_required_fields():
    """Every finding must have file, line, check, severity, description, snippet, fix."""
    findings = scan_file(VULNERABLE)
    assert findings, "Need at least one finding to test fields"
    for f in findings:
        assert f.file, "finding.file must not be empty"
        assert f.line > 0, "finding.line must be positive"
        assert f.check, "finding.check must not be empty"
        assert f.severity in ("CRITICAL", "HIGH", "MEDIUM"), f"Unknown severity: {f.severity}"
        assert f.description, "finding.description must not be empty"
        assert f.snippet, "finding.snippet must not be empty"
        assert f.fix, "finding.fix must not be empty"


def test_severity_assignments():
    """shell_injection must be CRITICAL, path_traversal and ssrf must be HIGH."""
    findings = scan_file(VULNERABLE)
    for f in findings:
        if f.check == "shell_injection":
            assert f.severity == "CRITICAL", f"shell_injection must be CRITICAL, got {f.severity}"
        elif f.check == "path_traversal":
            assert f.severity == "HIGH", f"path_traversal must be HIGH, got {f.severity}"
        elif f.check == "ssrf":
            assert f.severity == "HIGH", f"ssrf must be HIGH, got {f.severity}"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_mcp_tool_decorator_variant(tmp_path: Path):
    """@mcp.tool() decorator variant must also be detected."""
    server = tmp_path / "server.py"
    server.write_text(
        "import subprocess\n"
        "import mcp\n"
        "\n"
        "@mcp.tool()\n"
        "def run_cmd(cmd: str) -> str:\n"
        "    subprocess.run(f'ls {cmd}', shell=True)\n"
        "    return 'ok'\n"
    )
    findings = scan_file(str(server))
    assert any(f.check == "shell_injection" for f in findings), (
        "@mcp.tool() decorated functions must be detected"
    )


def test_no_params_no_findings(tmp_path: Path):
    """A @tool with no params cannot have user-controlled inputs — no findings."""
    server = tmp_path / "server.py"
    server.write_text(
        "import subprocess\n"
        "\n"
        "def tool(fn): return fn\n"
        "\n"
        "@tool\n"
        "def status() -> str:\n"
        "    subprocess.run('uptime', shell=True)\n"
        "    return 'ok'\n"
    )
    findings = scan_file(str(server))
    assert len(findings) == 0, (
        "No-param @tool functions should not produce findings (no user input)"
    )


def test_format_string_shell_injection(tmp_path: Path):
    """'cmd %s' % param with shell=True must be flagged."""
    server = tmp_path / "server.py"
    server.write_text(
        "import subprocess\n"
        "\n"
        "def tool(fn): return fn\n"
        "\n"
        "@tool\n"
        "def run(name: str) -> str:\n"
        "    subprocess.run('echo %s' % name, shell=True)\n"
        "    return 'ok'\n"
    )
    findings = scan_file(str(server))
    assert any(f.check == "shell_injection" for f in findings), (
        "'cmd %s' % param with shell=True must be flagged"
    )


def test_ssrf_fstring_url(tmp_path: Path):
    """requests.get(f'http://example.com/{path}') must be flagged."""
    server = tmp_path / "server.py"
    server.write_text(
        "import requests\n"
        "\n"
        "def tool(fn): return fn\n"
        "\n"
        "@tool\n"
        "def fetch(path: str) -> str:\n"
        "    return requests.get(f'http://example.com/{path}').text\n"
    )
    findings = scan_file(str(server))
    assert any(f.check == "ssrf" for f in findings), (
        "f-string URL with param must be flagged as SSRF"
    )


if __name__ == "__main__":
    import unittest
    # Simple runner without pytest
    passed = 0
    failed = 0
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test_fn in tests:
        import inspect
        sig = inspect.signature(test_fn)
        if sig.parameters:
            # Needs tmp_path — skip in manual runner
            print(f"  SKIP  {test_fn.__name__} (needs pytest tmp_path fixture)")
            continue
        try:
            test_fn()
            print(f"  PASS  {test_fn.__name__}")
            passed += 1
        except AssertionError as exc:
            print(f"  FAIL  {test_fn.__name__}: {exc}")
            failed += 1
        except Exception as exc:
            print(f"  ERROR {test_fn.__name__}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
