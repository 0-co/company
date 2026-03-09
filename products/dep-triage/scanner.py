#!/usr/bin/env python3
"""
dep-triage: Triage open dependency update PRs on a GitHub repository.

Usage:
    python3 scanner.py owner/repo
    python3 scanner.py https://github.com/owner/repo
    python3 scanner.py owner/repo --token ghp_xxxx
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

RISK_CRITICAL = "CRITICAL"
RISK_HIGH = "HIGH"
RISK_MEDIUM = "MEDIUM"
RISK_LOW = "LOW"

RISK_ORDER = {RISK_CRITICAL: 0, RISK_HIGH: 1, RISK_MEDIUM: 2, RISK_LOW: 3}

RECOMMENDATIONS = {
    RISK_CRITICAL: "Merge today",
    RISK_HIGH: "Review today",
    RISK_MEDIUM: "Review this week",
    RISK_LOW: "Safe to auto-merge",
}

DEP_BOT_AUTHORS = {"dependabot[bot]", "renovate[bot]", "dependabot-preview[bot]"}

# Patterns to extract package name + old/new versions from PR titles
VERSION_PATTERNS = [
    # "Bump lodash from 4.17.20 to 4.17.21"
    re.compile(
        r"[Bb]ump\s+(?P<pkg>[\w@/.-]+)\s+from\s+(?P<old>[\w.x*^~-]+)\s+to\s+(?P<new>[\w.x*^~-]+)",
        re.IGNORECASE,
    ),
    # "Update dependency axios to v1.7.0" (no old version)
    re.compile(
        r"[Uu]pdate\s+(?:dependency\s+)?(?P<pkg>[\w@/.-]+)\s+to\s+v?(?P<new>[\w.x*^~-]+)",
        re.IGNORECASE,
    ),
    # "Upgrade axios from 1.6.0 to 1.7.0"
    re.compile(
        r"[Uu]pgrade\s+(?P<pkg>[\w@/.-]+)\s+from\s+v?(?P<old>[\w.x*^~-]+)\s+to\s+v?(?P<new>[\w.x*^~-]+)",
        re.IGNORECASE,
    ),
    # "chore(deps): bump @types/node from 18.x to 20.x"
    re.compile(
        r"bump\s+(?P<pkg>[\w@/.-]+)\s+from\s+(?P<old>[\w.x*^~-]+)\s+to\s+(?P<new>[\w.x*^~-]+)",
        re.IGNORECASE,
    ),
]

CVE_GHSA_PATTERN = re.compile(r"(CVE-\d{4}-\d+|GHSA-[a-zA-Z0-9-]+)", re.IGNORECASE)
SECURITY_WORDS = re.compile(r"\b(security|vulnerability|vulnerabilities|exploit|patch)\b", re.IGNORECASE)
MAJOR_BUMP_WORDS = re.compile(r"\bmajor\b", re.IGNORECASE)
DEV_DEP_WORDS = re.compile(r"\b(devDependencies|dev.dep|@types/|eslint|prettier|jest|vitest|babel|webpack|rollup|vite)\b", re.IGNORECASE)


@dataclass
class VersionChange:
    old: str
    new: str
    is_major: bool = False
    is_minor: bool = False
    is_patch: bool = False


@dataclass
class DepPR:
    number: int
    title: str
    body: str
    author: str
    labels: list[str]
    created_at: str
    html_url: str
    package: str = ""
    version_change: Optional[VersionChange] = None
    risk: str = RISK_LOW
    reason: str = ""
    days_open: int = 0


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def make_request(url: str, token: Optional[str]) -> dict | list:
    """Fetch a URL from the GitHub API and return parsed JSON."""
    headers = {
        "User-Agent": "dep-triage-scanner/1.0",
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print(
                "ERROR: GitHub API rate limit exceeded. Pass --token to increase limits.",
                file=sys.stderr,
            )
        elif exc.code == 404:
            print(f"ERROR: Repository not found: {url}", file=sys.stderr)
        else:
            print(f"ERROR: HTTP {exc.code} fetching {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"ERROR: Network error fetching {url}: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def fetch_all_open_prs(repo: str, token: Optional[str]) -> list[dict]:
    """Fetch up to 5 pages of open PRs (100 per page) from GitHub API."""
    all_prs: list[dict] = []
    for page in range(1, 6):
        url = (
            f"https://api.github.com/repos/{repo}/pulls"
            f"?state=open&per_page=100&page={page}"
        )
        page_data = make_request(url, token)
        if not isinstance(page_data, list) or not page_data:
            break
        all_prs.extend(page_data)
        if len(page_data) < 100:
            break
    return all_prs


# ---------------------------------------------------------------------------
# PR parsing helpers
# ---------------------------------------------------------------------------

def parse_repo_arg(raw: str) -> str:
    """Normalize owner/repo or full GitHub URL to 'owner/repo'."""
    raw = raw.strip().rstrip("/")
    if raw.startswith("http://") or raw.startswith("https://"):
        parsed = urlparse(raw)
        # path looks like /owner/repo or /owner/repo/...
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2:
            print(f"ERROR: Cannot parse repo from URL: {raw}", file=sys.stderr)
            sys.exit(1)
        return f"{parts[0]}/{parts[1]}"
    if "/" not in raw:
        print(f"ERROR: Repo must be in 'owner/repo' format, got: {raw}", file=sys.stderr)
        sys.exit(1)
    return raw


def is_dep_pr(pr: dict) -> bool:
    """Return True if this PR looks like a dependency update."""
    author = pr.get("user", {}).get("login", "")
    if author in DEP_BOT_AUTHORS:
        return True

    title = pr.get("title", "").lower()
    label_names = [lbl["name"].lower() for lbl in pr.get("labels", [])]

    title_keywords = ("bump", "update", "upgrade")
    has_keyword = any(kw in title for kw in title_keywords)
    has_dep_label = any(
        dep in lbl for dep in ("dependencies", "dependency") for lbl in label_names
    )

    return has_keyword and has_dep_label


def extract_version_info(title: str) -> tuple[str, Optional[VersionChange]]:
    """Extract package name and version change from PR title."""
    for pattern in VERSION_PATTERNS:
        match = pattern.search(title)
        if match:
            groups = match.groupdict()
            package = groups.get("pkg", "")
            old_ver = groups.get("old", "")
            new_ver = groups.get("new", "")
            if package and new_ver:
                change = build_version_change(old_ver, new_ver)
                return package, change
    return "", None


def parse_semver(version: str) -> tuple[int, int, int]:
    """Extract (major, minor, patch) from a version string, ignoring prefixes/suffixes."""
    version = version.lstrip("v^~>=<")
    numeric = re.findall(r"\d+", version)
    major = int(numeric[0]) if len(numeric) > 0 else 0
    minor = int(numeric[1]) if len(numeric) > 1 else 0
    patch = int(numeric[2]) if len(numeric) > 2 else 0
    return major, minor, patch


def build_version_change(old_ver: str, new_ver: str) -> VersionChange:
    """Classify a version bump as major, minor, or patch."""
    change = VersionChange(old=old_ver, new=new_ver)
    if not old_ver:
        return change

    old_parts = parse_semver(old_ver)
    new_parts = parse_semver(new_ver)

    if new_parts[0] > old_parts[0]:
        change.is_major = True
    elif new_parts[1] > old_parts[1]:
        change.is_minor = True
    else:
        change.is_patch = True

    return change


def days_since(iso_timestamp: str) -> int:
    """Return number of days since an ISO 8601 UTC timestamp."""
    try:
        created = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        now = datetime.now(tz=timezone.utc)
        return (now - created).days
    except (ValueError, AttributeError):
        return 0


# ---------------------------------------------------------------------------
# Risk scoring
# ---------------------------------------------------------------------------

def score_risk(pr: DepPR) -> None:
    """Assign risk level and reason to a DepPR, mutating the object in place."""
    title = pr.title
    body = pr.body or ""
    combined = f"{title} {body}"
    label_names = [lbl.lower() for lbl in pr.labels]

    # CRITICAL: CVE/GHSA identifiers or "security" label
    cve_match = CVE_GHSA_PATTERN.search(combined)
    if cve_match or "security" in label_names:
        pr.risk = RISK_CRITICAL
        pr.reason = f"Security fix - {cve_match.group(0)}" if cve_match else "Security label"
        return

    # HIGH: security/vulnerability keywords in body, or major version bump
    if SECURITY_WORDS.search(body):
        pr.risk = RISK_HIGH
        pr.reason = "Security keywords in description"
        return

    if pr.version_change and pr.version_change.is_major:
        pr.risk = RISK_HIGH
        pr.reason = "Major version bump"
        return

    if MAJOR_BUMP_WORDS.search(title):
        pr.risk = RISK_HIGH
        pr.reason = "Major version bump (title)"
        return

    # MEDIUM: minor version bump
    if pr.version_change and pr.version_change.is_minor:
        pr.risk = RISK_MEDIUM
        pr.reason = "Minor version bump"
        return

    # LOW: patch bump, dev dependency, or no version info (default safe)
    if DEV_DEP_WORDS.search(combined) or DEV_DEP_WORDS.search(pr.package):
        pr.risk = RISK_LOW
        pr.reason = "Dev dependency"
        return

    if pr.version_change and pr.version_change.is_patch:
        pr.risk = RISK_LOW
        pr.reason = "Patch bump"
        return

    # Default fallback
    pr.risk = RISK_LOW
    pr.reason = "No version info, assumed safe"


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

RISK_COLORS = {
    RISK_CRITICAL: "\033[91m",  # bright red
    RISK_HIGH: "\033[93m",      # bright yellow
    RISK_MEDIUM: "\033[94m",    # bright blue
    RISK_LOW: "\033[92m",       # bright green
}
RESET = "\033[0m"


def format_version_display(pr: DepPR) -> str:
    """Build the version display string like '4.17.20->4.17.21'."""
    if not pr.version_change:
        return ""
    old = pr.version_change.old or "?"
    new = pr.version_change.new or "?"
    return f"{old}->{new}"


def supports_color() -> bool:
    """Return True if stdout appears to be a color-capable terminal."""
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def colorize(text: str, risk: str) -> str:
    if not supports_color():
        return text
    color = RISK_COLORS.get(risk, "")
    return f"{color}{text}{RESET}"


def print_report(repo: str, total_prs: int, dep_prs: list[DepPR]) -> None:
    """Print the formatted triage report to stdout."""
    sep = "=" * 60

    print(f"\nDEP TRIAGE REPORT -- {repo}")
    print(f"Scanned: {total_prs} open PRs | Dep PRs found: {len(dep_prs)}")
    print(sep)

    if not dep_prs:
        print("No dependency update PRs found.")
        print(sep)
        return

    sorted_prs = sorted(dep_prs, key=lambda p: RISK_ORDER[p.risk])

    for pr in sorted_prs:
        pr_num = f"#{pr.number}"
        risk_label = colorize(f"{pr.risk:<8}", pr.risk)
        pkg = pr.package or "(unknown package)"
        version_str = format_version_display(pr)
        pkg_ver = f"{pkg} {version_str}".strip()
        recommendation = RECOMMENDATIONS[pr.risk]
        days_label = f"{pr.days_open}d open"

        reason_str = f"[{pr.reason}]" if pr.reason else ""
        line = (
            f"{pr_num:<8} {risk_label} {pkg_ver:<35} "
            f"{reason_str:<35} {recommendation:<22} {days_label}"
        )
        print(line)

    print(sep)

    counts = {RISK_CRITICAL: 0, RISK_HIGH: 0, RISK_MEDIUM: 0, RISK_LOW: 0}
    for pr in dep_prs:
        counts[pr.risk] += 1

    print(
        f"Summary: {counts[RISK_CRITICAL]} critical, {counts[RISK_HIGH]} high, "
        f"{counts[RISK_MEDIUM]} medium, {counts[RISK_LOW]} safe"
    )

    actions = []
    if counts[RISK_CRITICAL]:
        actions.append(f"Merge {counts[RISK_CRITICAL]} CRITICAL PR(s) today.")
    if counts[RISK_HIGH]:
        actions.append(f"Review {counts[RISK_HIGH]} HIGH PR(s) today.")
    if counts[RISK_LOW]:
        actions.append(f"Batch {counts[RISK_LOW]} LOW PR(s) for auto-merge.")

    if actions:
        print("Action:", " ".join(actions))
    print()


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def build_dep_pr(raw_pr: dict) -> DepPR:
    """Convert a raw GitHub API PR dict into a DepPR dataclass."""
    labels = [lbl["name"] for lbl in raw_pr.get("labels", [])]
    created_at = raw_pr.get("created_at", "")
    package, version_change = extract_version_info(raw_pr.get("title", ""))

    pr = DepPR(
        number=raw_pr["number"],
        title=raw_pr.get("title", ""),
        body=raw_pr.get("body", "") or "",
        author=raw_pr.get("user", {}).get("login", ""),
        labels=labels,
        created_at=created_at,
        html_url=raw_pr.get("html_url", ""),
        package=package,
        version_change=version_change,
        days_open=days_since(created_at),
    )
    score_risk(pr)
    return pr


def run(repo: str, token: Optional[str]) -> None:
    """Main entry point: fetch PRs, triage, print report."""
    print(f"Fetching open PRs for {repo}...", file=sys.stderr)
    raw_prs = fetch_all_open_prs(repo, token)
    print(f"Fetched {len(raw_prs)} open PR(s).", file=sys.stderr)

    dep_prs = [build_dep_pr(pr) for pr in raw_prs if is_dep_pr(pr)]

    print_report(repo, len(raw_prs), dep_prs)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="scanner",
        description="Triage open dependency update PRs on a GitHub repository.",
    )
    parser.add_argument(
        "repo",
        help="GitHub repository as 'owner/repo' or full GitHub URL.",
    )
    parser.add_argument(
        "--token",
        metavar="TOKEN",
        default=None,
        help="GitHub personal access token (increases API rate limit).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo = parse_repo_arg(args.repo)
    run(repo, args.token)


if __name__ == "__main__":
    main()
