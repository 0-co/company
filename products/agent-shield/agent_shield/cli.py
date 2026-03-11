"""
Command-line interface for agent-shield.

Entry point: agent-shield

Commands:
  scan [directory]    Scan for security risks
  init [directory]    Create trusted manifest (manifest.json)
  verify [directory]  Verify against manifest.json
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

from .patterns import RISK_ORDER
from .scanner import Scanner, ScanResult, create_manifest, verify_manifest

# Risk levels ordered low → high for --min-risk filtering.
_RISK_LEVELS = ["low", "medium", "high", "critical"]

# Icons for text output.
_ICON = {
    "CLEAN": "\u2713",    # checkmark
    "LOW": "\u2139",      # info
    "MEDIUM": "\u26a0",   # warning
    "HIGH": "\u2718",     # cross
    "CRITICAL": "\u2718", # cross
}


def _risk_icon(level: str) -> str:
    return _ICON.get(level.upper(), "?")


def _passes_min_risk(level: str, min_risk: str) -> bool:
    """Return True if level is >= min_risk."""
    return RISK_ORDER.get(level.upper(), 0) >= RISK_ORDER.get(min_risk.upper(), 0)


def _format_text(results: List[ScanResult], min_risk: str, directory: str) -> str:
    lines: List[str] = []
    skill_count = len(results)
    lines.append(f"Scanning {skill_count} skill{'s' if skill_count != 1 else ''} in {directory}...")
    lines.append("")

    for result in results:
        icon = _risk_icon(result.risk_level)
        header = f"  {icon} {result.skill_name} \u2014 {result.risk_level}"
        lines.append(header)

        # Filter findings by min_risk.
        visible_findings = [
            f for f in result.findings
            if _passes_min_risk(f.risk_level, min_risk)
        ]

        for i, finding in enumerate(visible_findings):
            is_last = (i == len(visible_findings) - 1)
            branch = "\u2514\u2500" if is_last else "\u251c\u2500"
            lines.append(
                f"    {branch} {finding.file} [line {finding.line}]: "
                f"{finding.pattern_name} \u2014 {finding.description}"
            )
            lines.append(f'       "{finding.snippet}"')

    lines.append("")

    # Summary counts.
    counts: dict = {}
    for result in results:
        level = result.risk_level.upper()
        counts[level] = counts.get(level, 0) + 1

    summary_parts = []
    for level in ["CLEAN", "LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        if level in counts:
            summary_parts.append(f"{counts[level]} {level.lower()}")

    lines.append(f"Summary: {', '.join(summary_parts)}")
    lines.append("Run with --exit-code to fail CI on high/critical findings")

    return "\n".join(lines)


def _format_json(results: List[ScanResult], min_risk: str) -> str:
    output = []
    for result in results:
        visible_findings = [
            {
                "pattern_name": f.pattern_name,
                "risk_level": f.risk_level,
                "description": f.description,
                "file": f.file,
                "line": f.line,
                "snippet": f.snippet,
            }
            for f in result.findings
            if _passes_min_risk(f.risk_level, min_risk)
        ]
        output.append({
            "skill_name": result.skill_name,
            "path": result.path,
            "risk_level": result.risk_level,
            "findings": visible_findings,
        })
    return json.dumps(output, indent=2)


def _has_high_or_critical(results: List[ScanResult]) -> bool:
    for result in results:
        if result.risk_level in ("HIGH", "CRITICAL"):
            return True
    return False


def cmd_scan(args: argparse.Namespace) -> int:
    directory = str(Path(args.directory or ".").resolve())
    min_risk = (args.min_risk or "low").lower()
    output_format = (args.format or "text").lower()
    use_exit_code = bool(args.exit_code)

    scanner = Scanner()
    results = scanner.scan_directory(directory)

    if output_format == "json":
        print(_format_json(results, min_risk))
    else:
        print(_format_text(results, min_risk, directory))

    if use_exit_code and _has_high_or_critical(results):
        return 1
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    directory = str(Path(args.directory or ".").resolve())
    manifest = create_manifest(directory)
    manifest_path = Path(directory) / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    file_count = len(manifest["skills"])
    print(f"Manifest created: {manifest_path}")
    print(f"  {file_count} file{'s' if file_count != 1 else ''} recorded at {manifest['created_at']}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    directory = str(Path(args.directory or ".").resolve())
    output_format = (args.format or "text").lower()
    manifest_path = Path(directory) / "manifest.json"

    if not manifest_path.exists():
        print(
            f"error: no manifest.json found in {directory}. "
            "Run 'agent-shield init' first.",
            file=sys.stderr,
        )
        return 1

    with open(manifest_path, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)

    delta = verify_manifest(directory, manifest)

    if output_format == "json":
        print(json.dumps(delta, indent=2))
        return 1 if (delta["added"] or delta["removed"] or delta["modified"]) else 0

    created_at = manifest.get("created_at", "unknown")
    print(f"Verifying against manifest from {created_at}")
    print(f"  Directory: {directory}")
    print()

    changed = False

    if delta["added"]:
        changed = True
        print(f"  Added ({len(delta['added'])}):")
        for path in delta["added"]:
            print(f"    + {path}")

    if delta["removed"]:
        changed = True
        print(f"  Removed ({len(delta['removed'])}):")
        for path in delta["removed"]:
            print(f"    - {path}")

    if delta["modified"]:
        changed = True
        print(f"  Modified ({len(delta['modified'])}):")
        for path in delta["modified"]:
            print(f"    ~ {path}")

    if delta["unchanged"]:
        print(f"  Unchanged: {len(delta['unchanged'])} file{'s' if len(delta['unchanged']) != 1 else ''}")

    if not changed:
        print("All files match manifest. No tampering detected.")
        return 0

    print()
    print(f"WARNING: {len(delta['added']) + len(delta['removed']) + len(delta['modified'])} change(s) detected.")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-shield",
        description="Security scanner for AI agent skills and plugins.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  agent-shield scan ./skills\n"
            "  agent-shield scan --format json --min-risk high\n"
            "  agent-shield scan --exit-code\n"
            "  agent-shield init ./skills\n"
            "  agent-shield verify ./skills\n"
        ),
    )

    subparsers = parser.add_subparsers(dest="command")

    # scan
    scan_parser = subparsers.add_parser("scan", help="Scan for security risks")
    scan_parser.add_argument("directory", nargs="?", help="Directory to scan (default: current dir)")
    scan_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    scan_parser.add_argument(
        "--min-risk",
        choices=_RISK_LEVELS,
        default="low",
        help="Only show findings at this level or above",
    )
    scan_parser.add_argument(
        "--exit-code",
        action="store_true",
        help="Exit with code 1 if HIGH or CRITICAL findings exist",
    )

    # init
    init_parser = subparsers.add_parser("init", help="Create trusted manifest (manifest.json)")
    init_parser.add_argument("directory", nargs="?", help="Directory to hash (default: current dir)")
    init_parser.add_argument("--format", choices=["text", "json"], default="text")

    # verify
    verify_parser = subparsers.add_parser("verify", help="Verify files against manifest.json")
    verify_parser.add_argument("directory", nargs="?", help="Directory to verify (default: current dir)")
    verify_parser.add_argument("--format", choices=["text", "json"], default="text")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "scan": cmd_scan,
        "init": cmd_init,
        "verify": cmd_verify,
    }

    handler = dispatch.get(args.command)
    if handler is None:
        parser.print_help()
        sys.exit(1)

    sys.exit(handler(args))


if __name__ == "__main__":
    main()
