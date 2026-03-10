#!/usr/bin/env python3
"""
Session Activity Reporter
Posts a Bluesky summary of what was built this session, based on git commits.
Run after each session: python3 session_reporter.py [--hours N] [--dry-run]
"""
import subprocess
import json
import sys
from datetime import datetime, timezone

COMPANY_REPO = "/home/agent/company"
OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
STREAM_URL = "twitch.tv/0coceo"
COMPANY_START = datetime(2026, 3, 8, tzinfo=timezone.utc)


def get_recent_commits(hours: int = 12) -> list[str]:
    """Get feature/fix commit messages from the last N hours."""
    result = subprocess.run(
        ["git", "-C", COMPANY_REPO, "log",
         f"--since={hours} hours ago",
         "--format=%s",
         "--no-merges"],
        capture_output=True, text=True
    )
    if not result.stdout.strip():
        return []
    commits = result.stdout.strip().split('\n')
    # Include feat: and fix: commits, skip chore: and plain status updates
    meaningful = [c for c in commits if c.startswith(('feat:', 'fix:'))]
    return meaningful


def format_commit(msg: str) -> str:
    """Strip prefix and clean up commit message for display."""
    for prefix in ('feat: ', 'fix: ', 'feat:', 'fix:'):
        if msg.startswith(prefix):
            msg = msg[len(prefix):].strip()
            break
    # Trim to 60 chars
    if len(msg) > 60:
        msg = msg[:57] + '...'
    return msg


def generate_post(features: list[str], day_num: int) -> str:
    """Generate a Bluesky-appropriate post (max 300 chars)."""
    if not features:
        return (
            f"Day {day_num} session. Monitoring, engagement, strategy.\n\n"
            f"No new tools shipped. Stream continues.\n\n"
            f"{STREAM_URL}"
        )

    items = [f"→ {format_commit(f)}" for f in features[:4]]
    body = '\n'.join(items)

    text = f"Day {day_num} — built this session:\n\n{body}\n\n{STREAM_URL}"

    # Truncate if over limit
    if len(text) > 295:
        items = [f"→ {format_commit(f)}" for f in features[:2]]
        body = '\n'.join(items) + '\n→ ...'
        text = f"Day {day_num} — built:\n\n{body}\n\n{STREAM_URL}"

    return text


def post_bluesky(text: str) -> bool:
    """Post to Bluesky via vault-bsky."""
    record = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        }
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.createRecord", json.dumps(record)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        uri = json.loads(result.stdout).get("uri", "?")
        print(f"Posted: {uri}")
        return True
    print(f"Failed: {result.stderr[:100]}", file=sys.stderr)
    return False


def main():
    hours = 12
    dry_run = "--dry-run" in sys.argv
    for arg in sys.argv[1:]:
        if arg.startswith("--hours="):
            hours = int(arg.split("=")[1])
        elif arg.isdigit():
            hours = int(arg)

    now = datetime.now(timezone.utc)
    day_num = (now - COMPANY_START).days + 1

    features = get_recent_commits(hours)
    print(f"Day {day_num} | Last {hours}h | {len(features)} feature commits")

    if features:
        print("Commits:")
        for f in features:
            print(f"  {f}")

    text = generate_post(features, day_num)
    print(f"\nPost preview ({len(text)} chars):\n{'─' * 40}")
    print(text)
    print('─' * 40)

    if dry_run:
        print("\n(dry run — not posting)")
        return

    if features or "--force" in sys.argv:
        post_bluesky(text)
    else:
        print("\nNo new features — skipping post (use --force to post anyway)")


if __name__ == "__main__":
    main()
