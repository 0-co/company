"""mcp-patch CLI entry point."""

import argparse
import sys
from pathlib import Path

from mcp_patch.scanner import Finding, scan_file

# ANSI color codes
_RED = "\033[31m"
_YELLOW = "\033[33m"
_CYAN = "\033[36m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_RESET = "\033[0m"

_SEVERITY_COLOR = {
    "CRITICAL": _RED + _BOLD,
    "HIGH": _YELLOW + _BOLD,
    "MEDIUM": _CYAN + _BOLD,
}


def _supports_color() -> bool:
    return sys.stdout.isatty()


def _color(text: str, code: str) -> str:
    if _supports_color():
        return f"{code}{text}{_RESET}"
    return text


def _format_severity(severity: str) -> str:
    code = _SEVERITY_COLOR.get(severity, "")
    # Pad to 8 chars for alignment
    padded = severity.ljust(8)
    return _color(padded, code)


def _print_finding(finding: Finding) -> None:
    check = _color(finding.check, _BOLD)
    print(f"  {_format_severity(finding.severity)} {check}  line {finding.line}")
    print(f"  {finding.snippet}")
    print(f"  {_color(finding.description, _DIM)}")
    print(f"  Fix: {finding.fix}")
    print()


def cmd_scan(args: argparse.Namespace) -> int:
    """Run the scan subcommand. Returns exit code."""
    all_findings: list[Finding] = []
    files_scanned = 0
    errors: list[str] = []

    targets = _expand_targets(args.files)

    for target in targets:
        print(f"Scanning {target}...")
        try:
            findings = scan_file(target)
        except RuntimeError as exc:
            errors.append(str(exc))
            continue

        files_scanned += 1
        all_findings.extend(findings)

        if findings:
            print()
            for finding in findings:
                _print_finding(finding)

    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)

    _print_summary(all_findings, files_scanned)

    # Non-zero exit if any findings
    return 1 if all_findings else 0


def _expand_targets(files: list[str]) -> list[str]:
    """Expand directories to Python files; pass through regular file paths."""
    targets: list[str] = []
    for file_arg in files:
        path = Path(file_arg)
        if path.is_dir():
            targets.extend(str(p) for p in sorted(path.rglob("*.py")))
        else:
            targets.append(file_arg)
    return targets


def _print_summary(findings: list[Finding], files_scanned: int) -> None:
    count = len(findings)
    if count == 0:
        status = _color("No issues found.", _BOLD)
        print(f"{status} ({files_scanned} file{'s' if files_scanned != 1 else ''} scanned)")
    else:
        by_severity: dict[str, int] = {}
        for finding in findings:
            by_severity[finding.severity] = by_severity.get(finding.severity, 0) + 1

        parts = []
        for severity in ("CRITICAL", "HIGH", "MEDIUM"):
            if severity in by_severity:
                n = by_severity[severity]
                parts.append(_color(f"{n} {severity}", _SEVERITY_COLOR.get(severity, "")))

        summary = ", ".join(parts)
        file_word = "file" if files_scanned == 1 else "files"
        issue_word = "issue" if count == 1 else "issues"
        print(f"Found {count} {issue_word} ({summary}) in {files_scanned} {file_word}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mcp-patch",
        description="Security scanner for Python MCP server code.",
    )
    sub = parser.add_subparsers(dest="command")

    scan_parser = sub.add_parser("scan", help="Scan Python files for vulnerabilities")
    scan_parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="Python files or directories to scan",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        sys.exit(cmd_scan(args))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
