"""
Core scanning logic for agent-shield.

Provides Scanner, ScanResult, Finding, create_manifest, and verify_manifest.
"""

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .patterns import (
    MCP_COMMAND,
    MCP_ENV,
    RISK_ORDER,
    SCANNABLE_EXTENSIONS,
    higher_risk,
    patterns_for_extension,
)

# Maximum bytes read per file to avoid memory issues on large files.
MAX_FILE_BYTES = 1 * 1024 * 1024  # 1 MB

# Maximum characters shown in a snippet.
SNIPPET_MAX_LENGTH = 120

# Regex that matches long hex strings or base64-like values likely to be real secrets.
_SECRET_VALUE_RE = re.compile(r"\b[A-Fa-f0-9]{32,}\b|[A-Za-z0-9+/]{40,}={0,2}")


@dataclass
class Finding:
    pattern_name: str
    risk_level: str
    description: str
    file: str        # relative path within the skill directory
    line: int
    snippet: str     # truncated matched line, safe to display


@dataclass
class ScanResult:
    skill_name: str
    path: str
    risk_level: str = "CLEAN"
    findings: List[Finding] = field(default_factory=list)

    def add_finding(self, finding: Finding) -> None:
        self.findings.append(finding)
        self.risk_level = higher_risk(self.risk_level, finding.risk_level)


def _redact_snippet(text: str) -> str:
    """Replace long hex/base64 strings with [REDACTED] and truncate to SNIPPET_MAX_LENGTH."""
    redacted = _SECRET_VALUE_RE.sub("[REDACTED]", text)
    if len(redacted) > SNIPPET_MAX_LENGTH:
        redacted = redacted[:SNIPPET_MAX_LENGTH] + "..."
    return redacted.strip()


def _read_file_text(filepath: Path) -> Optional[str]:
    """Read a file as text, up to MAX_FILE_BYTES. Returns None on encoding errors."""
    try:
        raw = filepath.read_bytes()
    except OSError:
        return None

    if len(raw) > MAX_FILE_BYTES:
        raw = raw[:MAX_FILE_BYTES]

    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        # Skip binary files.
        return None


def _scan_file(filepath: Path, skill_root: Path) -> List[Finding]:
    """Apply appropriate patterns to a single file. Returns list of findings."""
    extension = filepath.suffix.lower()
    patterns = patterns_for_extension(extension)
    if not patterns:
        return []

    text = _read_file_text(filepath)
    if text is None:
        return []

    relative_path = str(filepath.relative_to(skill_root))
    findings: List[Finding] = []

    for line_number, line_text in enumerate(text.splitlines(), start=1):
        for pattern_name, regex, risk_level, description in patterns:
            if re.search(regex, line_text, re.IGNORECASE):
                findings.append(Finding(
                    pattern_name=pattern_name,
                    risk_level=risk_level,
                    description=description,
                    file=relative_path,
                    line=line_number,
                    snippet=_redact_snippet(line_text),
                ))

    return findings


def _scan_mcp_config(filepath: Path, label: str) -> ScanResult:
    """
    Scan an MCP config JSON file (e.g. claude_desktop_config.json) for
    malicious server configurations.

    Checks each server in ``mcpServers`` for dangerous command/args patterns
    and suspicious env var values.
    """
    result = ScanResult(skill_name=label, path=str(filepath))

    text = _read_file_text(filepath)
    if text is None:
        return result

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return result

    mcp_servers = data.get("mcpServers", {})
    if not isinstance(mcp_servers, dict) or not mcp_servers:
        return result

    relative_path = filepath.name  # just the filename as context

    for server_name, config in mcp_servers.items():
        if not isinstance(config, dict):
            continue

        command = config.get("command", "")
        args = config.get("args", [])
        env = config.get("env", {})

        # Build a combined string for command + args checks.
        args_list = [str(a) for a in args] if isinstance(args, list) else []
        cmd_str = " ".join([command] + args_list)

        for pattern_name, regex, risk_level, description in MCP_COMMAND:
            if re.search(regex, cmd_str, re.IGNORECASE):
                result.add_finding(Finding(
                    pattern_name=pattern_name,
                    risk_level=risk_level,
                    description=f"server '{server_name}': {description}",
                    file=relative_path,
                    line=0,
                    snippet=_redact_snippet(cmd_str),
                ))

        # Check each env var value.
        if isinstance(env, dict):
            for env_key, env_val in env.items():
                env_str = f"{env_key}={env_val}"
                for pattern_name, regex, risk_level, description in MCP_ENV:
                    if re.search(regex, env_str, re.IGNORECASE):
                        result.add_finding(Finding(
                            pattern_name=pattern_name,
                            risk_level=risk_level,
                            description=f"server '{server_name}': {description}",
                            file=relative_path,
                            line=0,
                            snippet=_redact_snippet(env_str),
                        ))

    return result


class Scanner:
    """Scans skill directories or individual skill paths for security risks."""

    def scan_skill(self, path: str, skill_name: Optional[str] = None) -> ScanResult:
        """Scan a single skill directory or file."""
        skill_path = Path(path).resolve()
        name = skill_name or skill_path.name
        result = ScanResult(skill_name=name, path=str(skill_path))

        if skill_path.is_file():
            if skill_path.suffix.lower() in SCANNABLE_EXTENSIONS:
                for finding in _scan_file(skill_path, skill_path.parent):
                    result.add_finding(finding)
            return result

        if not skill_path.is_dir():
            return result

        for filepath in sorted(skill_path.rglob("*")):
            if not filepath.is_file():
                continue
            if filepath.suffix.lower() not in SCANNABLE_EXTENSIONS:
                continue
            for finding in _scan_file(filepath, skill_path):
                result.add_finding(finding)

        return result

    def scan_mcp_configs(self, *paths: str) -> List[ScanResult]:
        """
        Scan one or more MCP config JSON files for malicious server configs.

        If no paths are provided, checks common default locations:
        ``~/.claude/settings.json``, ``~/Library/Application Support/Claude/claude_desktop_config.json``,
        and ``./mcp.json``.

        Returns a list of ScanResult, one per file found.
        """
        if not paths:
            home = Path.home()
            candidates = [
                home / ".claude" / "settings.json",
                home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
                Path.cwd() / "mcp.json",
                Path.cwd() / "claude_desktop_config.json",
            ]
        else:
            candidates = [Path(p).resolve() for p in paths]

        results: List[ScanResult] = []
        for candidate in candidates:
            if candidate.is_file():
                label = str(candidate)
                results.append(_scan_mcp_config(candidate, label))

        return results

    def scan_directory(self, path: str) -> List[ScanResult]:
        """Scan all subdirectories as separate skills, plus any scannable root files."""
        root = Path(path).resolve()
        results: List[ScanResult] = []

        if not root.is_dir():
            print(f"error: {path} is not a directory", file=sys.stderr)
            return results

        # Each direct subdirectory is treated as a separate skill.
        subdirs = sorted(entry for entry in root.iterdir() if entry.is_dir())
        for subdir in subdirs:
            results.append(self.scan_skill(str(subdir)))

        # Root-level files (no subdirectory) are grouped as a single implicit skill.
        root_files = [
            entry for entry in root.iterdir()
            if entry.is_file() and entry.suffix.lower() in SCANNABLE_EXTENSIONS
        ]
        if root_files:
            root_result = ScanResult(skill_name="(root)", path=str(root))
            for filepath in sorted(root_files):
                for finding in _scan_file(filepath, root):
                    root_result.add_finding(finding)
            results.append(root_result)

        return results


# ---------------------------------------------------------------------------
# Integrity manifest
# ---------------------------------------------------------------------------

def _file_sha256(filepath: Path) -> str:
    """Compute SHA-256 of a file. Reads in chunks to handle large files."""
    digest = hashlib.sha256()
    try:
        with filepath.open("rb") as fh:
            while True:
                chunk = fh.read(65536)
                if not chunk:
                    break
                digest.update(chunk)
    except OSError:
        return ""
    return digest.hexdigest()


def _should_hash(filepath: Path, root: Path) -> bool:
    """Return True if the file should be included in a manifest."""
    if filepath.suffix.lower() not in SCANNABLE_EXTENSIONS:
        return False
    # Exclude the manifest file itself.
    if filepath.name == "manifest.json" and filepath.parent == root:
        return False
    return True


def create_manifest(directory: str) -> Dict:
    """
    Walk directory, compute SHA-256 of each scannable skill file.

    Returns a dict suitable for JSON serialization:
      {
        "created_at": "ISO timestamp",
        "directory": "/absolute/path",
        "skills": {"skill_name/file.py": "sha256hex", ...}
      }
    """
    root = Path(directory).resolve()
    skills: Dict[str, str] = {}

    for filepath in sorted(root.rglob("*")):
        if not filepath.is_file():
            continue
        if not _should_hash(filepath, root):
            continue
        relative = str(filepath.relative_to(root))
        skills[relative] = _file_sha256(filepath)

    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "directory": str(root),
        "skills": skills,
    }


def verify_manifest(directory: str, manifest: Dict) -> Dict:
    """
    Compare current file hashes to a manifest produced by create_manifest.

    Returns:
      {
        "added":     [...],   # files present now but not in manifest
        "removed":   [...],   # files in manifest but not present now
        "modified":  [...],   # files present in both but hash differs
        "unchanged": [...],   # files present in both with matching hash
      }
    """
    root = Path(directory).resolve()
    recorded: Dict[str, str] = manifest.get("skills", {})

    current: Dict[str, str] = {}
    for filepath in sorted(root.rglob("*")):
        if not filepath.is_file():
            continue
        if not _should_hash(filepath, root):
            continue
        relative = str(filepath.relative_to(root))
        current[relative] = _file_sha256(filepath)

    recorded_keys = set(recorded)
    current_keys = set(current)

    added = sorted(current_keys - recorded_keys)
    removed = sorted(recorded_keys - current_keys)
    modified = sorted(
        key for key in current_keys & recorded_keys
        if current[key] != recorded[key]
    )
    unchanged = sorted(
        key for key in current_keys & recorded_keys
        if current[key] == recorded[key]
    )

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
    }
