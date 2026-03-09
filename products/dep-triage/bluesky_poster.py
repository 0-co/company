#!/usr/bin/env python3
"""
bluesky_poster.py — Scan top npm repos for unpatched security dependency PRs
and post a daily summary to Bluesky.

Usage:
    python3 bluesky_poster.py daily   # Scan and post to Bluesky
    python3 bluesky_poster.py test    # Scan and print what would be posted
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BLUESKY_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
BLUESKY_HANDLE = "0coceo.bsky.social"
VAULT_BSKY = "/home/vault/bin/vault-bsky"

REPOS = [
    "facebook/react",
    "nestjs/nest",
    "vuejs/vue",
    "expressjs/express",
    "axios/axios",
    "lodash/lodash",
    "moment/moment",
    "webpack/webpack",
]

# Keywords in PR title/body that indicate a security-relevant dependency update
SECURITY_KEYWORDS = [
    "CVE-",
    "GHSA-",
    "security",
    "vulnerability",
    "vuln",
    "critical",
    "high severity",
    "RCE",
    "injection",
    "XSS",
]

SECURITY_PATTERN = re.compile(
    "|".join(re.escape(kw) for kw in SECURITY_KEYWORDS),
    re.IGNORECASE,
)

PROMO_LINK = "github.com/0-co/company"
HASHTAGS = "#devsec #dependabot"

VAULT_GH = "/home/vault/bin/vault-gh"


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class SecurityPR:
    number: int
    title: str
    created_at: str
    html_url: str
    days_open: int
    matched_keyword: str


@dataclass
class RepoFindings:
    repo: str
    total_dep_prs: int
    security_prs: list[SecurityPR]
    oldest_security_pr: Optional[SecurityPR]


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

def log(message: str) -> None:
    """Write a timestamped log line to stdout."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{timestamp}] {message}")


def log_error(message: str) -> None:
    """Write a timestamped error line to stderr."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{timestamp}] ERROR: {message}", file=sys.stderr)


# ---------------------------------------------------------------------------
# GitHub API via vault-gh
# ---------------------------------------------------------------------------

def fetch_dependency_prs(repo: str) -> Optional[list[dict]]:
    """
    Fetch open PRs labeled 'dependencies' for a repo via vault-gh.
    Returns None on failure so the caller can skip and continue.
    """
    endpoint = f"/repos/{repo}/pulls?state=open&labels=dependencies&per_page=30"
    try:
        result = subprocess.run(
            ["sudo", "-u", "vault", VAULT_GH, "api", endpoint],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        log_error(f"Timeout fetching PRs for {repo}")
        return None
    except FileNotFoundError:
        log_error(f"vault-gh not found at {VAULT_GH}")
        return None

    if result.returncode != 0:
        log_error(f"vault-gh failed for {repo}: {result.stderr.strip()}")
        return None

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        log_error(f"JSON parse error for {repo}: {exc}")
        return None

    if not isinstance(data, list):
        log_error(f"Unexpected response shape for {repo}: {type(data)}")
        return None

    return data


# ---------------------------------------------------------------------------
# PR analysis
# ---------------------------------------------------------------------------

def days_since(iso_timestamp: str) -> int:
    """Return number of whole days elapsed since an ISO 8601 UTC timestamp."""
    try:
        created = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        delta = datetime.now(tz=timezone.utc) - created
        return delta.days
    except (ValueError, AttributeError):
        return 0


def find_security_keyword(text: str) -> str:
    """Return the first security keyword found in text, or empty string."""
    match = SECURITY_PATTERN.search(text)
    return match.group(0) if match else ""


def is_security_pr(pr: dict) -> tuple[bool, str]:
    """
    Check if a PR title or body contains security keywords.
    Returns (is_security, matched_keyword).
    """
    combined = (pr.get("title", "") + " " + (pr.get("body", "") or "")).strip()
    keyword = find_security_keyword(combined)
    return bool(keyword), keyword


def analyze_repo(repo: str, raw_prs: list[dict]) -> RepoFindings:
    """Extract security PRs from a list of raw GitHub PR dicts."""
    security_prs: list[SecurityPR] = []

    for raw in raw_prs:
        flagged, keyword = is_security_pr(raw)
        if not flagged:
            continue

        created_at = raw.get("created_at", "")
        security_prs.append(SecurityPR(
            number=raw.get("number", 0),
            title=raw.get("title", ""),
            created_at=created_at,
            html_url=raw.get("html_url", ""),
            days_open=days_since(created_at),
            matched_keyword=keyword,
        ))

    oldest: Optional[SecurityPR] = None
    if security_prs:
        oldest = max(security_prs, key=lambda p: p.days_open)

    return RepoFindings(
        repo=repo,
        total_dep_prs=len(raw_prs),
        security_prs=security_prs,
        oldest_security_pr=oldest,
    )


# ---------------------------------------------------------------------------
# Post formatting
# ---------------------------------------------------------------------------

def format_repo_short(repo: str) -> str:
    """Return just the repo name part (drop the owner prefix)."""
    return repo.split("/")[-1]


def format_post_text(findings: RepoFindings) -> str:
    """
    Build the Bluesky post text for a repo finding.
    Keeps the result under 280 graphemes.
    """
    repo_short = format_repo_short(findings.repo)
    count = len(findings.security_prs)
    oldest = findings.oldest_security_pr

    if oldest:
        days = oldest.days_open
        body = (
            f"Security PRs ignored: {repo_short} has {count} open dependency "
            f"PR{'s' if count != 1 else ''}, oldest {days} days.\n"
            f"Run DepTriage to find which ones are critical: {PROMO_LINK}\n"
            f"{HASHTAGS}"
        )
    else:
        body = (
            f"Security check: {repo_short} has {count} open dependency "
            f"PR{'s' if count != 1 else ''} flagged for review.\n"
            f"Run DepTriage to find which ones are critical: {PROMO_LINK}\n"
            f"{HASHTAGS}"
        )

    # Truncate to 280 graphemes if needed (rare, but be safe)
    if len(body) > 280:
        cutoff = 280 - len(f"\n{PROMO_LINK}\n{HASHTAGS}") - 1
        body = body[:cutoff].rstrip() + "\n" + PROMO_LINK + "\n" + HASHTAGS

    return body


def pick_best_finding(all_findings: list[RepoFindings]) -> Optional[RepoFindings]:
    """
    Select the most interesting finding to post about.
    Priority: most security PRs, then oldest unaddressed PR.
    """
    candidates = [f for f in all_findings if f.security_prs]
    if not candidates:
        return None

    # Sort by: number of security PRs (desc), then oldest PR age (desc)
    candidates.sort(
        key=lambda f: (
            len(f.security_prs),
            f.oldest_security_pr.days_open if f.oldest_security_pr else 0,
        ),
        reverse=True,
    )
    return candidates[0]


# ---------------------------------------------------------------------------
# Bluesky posting
# ---------------------------------------------------------------------------

def post_to_bluesky(text: str) -> bool:
    """
    Post text to Bluesky via vault-bsky.
    Returns True on success, False on failure.
    """
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {
        "repo": BLUESKY_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": created_at,
        },
    }

    try:
        result = subprocess.run(
            [
                "sudo", "-u", "vault", VAULT_BSKY,
                "com.atproto.repo.createRecord",
                json.dumps(record),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        log_error("Timeout posting to Bluesky")
        return False
    except FileNotFoundError:
        log_error(f"vault-bsky not found at {VAULT_BSKY}")
        return False

    if result.returncode != 0:
        log_error(f"vault-bsky failed (exit {result.returncode}): {result.stderr.strip()}")
        if result.stdout.strip():
            log_error(f"stdout: {result.stdout.strip()}")
        return False

    log(f"Bluesky post successful. Response: {result.stdout.strip()[:200]}")
    return True


# ---------------------------------------------------------------------------
# Main scan pipeline
# ---------------------------------------------------------------------------

def scan_all_repos() -> list[RepoFindings]:
    """Scan all configured repos and return their findings."""
    all_findings: list[RepoFindings] = []

    for repo in REPOS:
        log(f"Scanning {repo}...")
        raw_prs = fetch_dependency_prs(repo)

        if raw_prs is None:
            log(f"Skipping {repo} due to API error.")
            continue

        findings = analyze_repo(repo, raw_prs)
        all_findings.append(findings)

        log(
            f"  {repo}: {findings.total_dep_prs} dep PRs, "
            f"{len(findings.security_prs)} security-flagged"
        )
        if findings.oldest_security_pr:
            log(
                f"  Oldest security PR: #{findings.oldest_security_pr.number} "
                f"({findings.oldest_security_pr.days_open} days) — "
                f"{findings.oldest_security_pr.title[:60]}"
            )

    return all_findings


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

def run_daily() -> None:
    """Scan repos and post the best finding to Bluesky."""
    log("Starting daily Bluesky post run.")

    all_findings = scan_all_repos()

    if not all_findings:
        log_error("No findings collected. Aborting post.")
        sys.exit(1)

    best = pick_best_finding(all_findings)

    if best is None:
        log("No security PRs found across any scanned repos. Nothing to post.")
        return

    post_text = format_post_text(best)
    log(f"Selected repo for post: {best.repo}")
    log(f"Post text ({len(post_text)} chars):\n---\n{post_text}\n---")

    success = post_to_bluesky(post_text)
    if not success:
        log_error("Failed to post to Bluesky.")
        sys.exit(1)

    log("Daily run complete.")


def run_test() -> None:
    """Scan repos and print what would be posted, without actually posting."""
    log("Running in TEST mode — no post will be made.")

    all_findings = scan_all_repos()

    if not all_findings:
        log_error("No findings collected.")
        return

    log("\n--- Scan Summary ---")
    for findings in all_findings:
        status = f"{len(findings.security_prs)} security PRs" if findings.security_prs else "none flagged"
        log(f"  {findings.repo}: {findings.total_dep_prs} dep PRs, {status}")

    best = pick_best_finding(all_findings)

    if best is None:
        log("No security PRs found. Nothing would be posted.")
        return

    post_text = format_post_text(best)

    log(f"\n--- Would Post (selected: {best.repo}) ---")
    log(f"Character count: {len(post_text)}/280")
    print()
    print(post_text)
    print()
    log("Test run complete. No post was made.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("daily", "test"):
        print("Usage: python3 bluesky_poster.py [daily|test]", file=sys.stderr)
        print("  daily  — Scan repos and post to Bluesky", file=sys.stderr)
        print("  test   — Scan repos and print what would be posted", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "daily":
        run_daily()
    elif mode == "test":
        run_test()


if __name__ == "__main__":
    main()
