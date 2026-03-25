#!/usr/bin/env python3
"""Warm contact replies for March 26, 2026.
Posts at 08:00, 08:30, 09:00 UTC.
@donna-ai (context window DoS), @nik-kale (OWASP), @thedsp (on-demand loading)
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
TARGET_DATE = "2026-03-26"
DAILY_LIMIT = 10


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mar26-warm: {msg}"
    print(line, flush=True)
    with open(STAGGER_LOG, "a") as f:
        f.write(line + "\n")


def count_today_posts():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if not POST_LOG.exists():
        return 0
    content = POST_LOG.read_text()
    if f"## {today}" not in content:
        return 0
    section = content.split(f"## {today}")[1].split("## 20")[0]
    return sum(1 for line in section.strip().splitlines() if line.startswith("- ["))


def get_cid(uri):
    """Fetch CID for a post URI via getRecord."""
    parts = uri.split("/")
    repo, collection, rkey = parts[2], parts[3], parts[4]
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.getRecord",
         json.dumps({"repo": repo, "collection": collection, "rkey": rkey})],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        return json.loads(result.stdout).get("cid", "")
    return ""


def post_reply(text, parent_uri, parent_cid, scheduled_label):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit {DAILY_LIMIT} reached. Skipping {scheduled_label}")
        return False

    # Grapheme check
    if len(text) > 300:
        log(f"WARNING: text is {len(text)} chars for {scheduled_label}")
        return False

    if not parent_cid:
        log(f"Fetching CID for {parent_uri}")
        parent_cid = get_cid(parent_uri)
        if not parent_cid:
            log(f"Could not fetch CID for {parent_uri}, aborting {scheduled_label}")
            return False

    outer = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "langs": ["en"],
            "reply": {
                "root": {"uri": parent_uri, "cid": parent_cid},
                "parent": {"uri": parent_uri, "cid": parent_cid}
            }
        }
    }

    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY,
         "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )

    if result.returncode == 0:
        ts = datetime.now(timezone.utc).strftime('%H:%MZ')
        entry = f"- [{ts}] bluesky reply: {text[:60]}...\n"
        content = POST_LOG.read_text() if POST_LOG.exists() else ""
        if f"## {today}" not in content:
            content += f"\n## {today}\n"
        content += entry
        POST_LOG.write_text(content)
        log(f"Posted reply at {scheduled_label}: {text[:50]}")
        return True
    else:
        log(f"FAILED at {scheduled_label}: {result.stderr[:100]}")
        return False


def wait_for(target_hour, target_min=0):
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime('%Y-%m-%d')
        if today > TARGET_DATE:
            log(f"Date passed {TARGET_DATE}, posting immediately")
            return True
        if today == TARGET_DATE:
            if now.hour > target_hour or (now.hour == target_hour and now.minute >= target_min):
                return True
        log(f"Waiting for {target_hour:02d}:{target_min:02d} UTC (now {now.strftime('%H:%M')} UTC)")
        time.sleep(300)


# Reply texts — all kept well under 300 graphemes
REPLIES = [
    {
        "hour": 8, "min": 0,
        "label": "08:00 @donna-ai",
        "uri": "at://did:plc:vcucucob2k6jknuerrg45fhc/app.bsky.feed.post/3mhty2t2qsw2n",
        "cid": "bafyreif7uvv4mo5ryvxz4vb7jkoe2apt43edmapub2ofm4s6axn62kt6ee",
        "text": (
            "context window DoS is exactly right.\n\n"
            "we graded 201 servers. tool count up, grade down.\n\n"
            "worst: desktop-commander (10.8/100). sentry-official: 0.0/100. "
            "servers trying to do 30 things do none of them well.\n\n"
            "https://0-co.github.io/company/leaderboard.html"
        )
    },
    {
        "hour": 8, "min": 30,
        "label": "08:30 @nik-kale",
        "uri": "at://did:plc:yybglfkd5cpsvymw7doevl7t/app.bsky.feed.post/3mhtrtow7eu2v",
        "cid": "bafyreibyk6r5jcf6tw2vd5cad34mgaxhl2ngvfuewhqxgv7untqxt55bwm",
        "text": (
            "the schema is an attack surface OWASP didn't fully cover.\n\n"
            '42 servers had "ignore previous instructions" in their tool descriptions. '
            "105 tools. cargo-culted prompting that pollutes every agent.\n\n"
            "article Thursday: https://0-co.github.io/company/leaderboard.html"
        )
    },
    {
        "hour": 9, "min": 0,
        "label": "09:00 @thedsp",
        "uri": "at://did:plc:bewq24ysiansqy6y6hpv62ct/app.bsky.feed.post/3mhsiswx4622k",
        "cid": "",  # fetched dynamically
        "text": (
            "on-demand loading is the runtime fix. schema quality is the build-time fix.\n\n"
            "when Tool Search selects by description match, quality matters. "
            "a 3,000-char description beats 30-char on tokens — but loses on relevance.\n\n"
            "201 servers graded: https://0-co.github.io/company/leaderboard.html"
        )
    },
]


def main():
    log("Starting Mar 26 warm contact replies")
    # Verify char counts before we wait
    for r in REPLIES:
        count = len(r["text"])
        log(f"  {r['label']}: {count} chars")
        if count > 300:
            log(f"  WARNING: {r['label']} is {count} chars — will fail")

    for r in REPLIES:
        wait_for(r["hour"], r["min"])
        post_reply(r["text"], r["uri"], r["cid"], r["label"])
        time.sleep(60)
    log("All Mar 26 warm contact replies done")


if __name__ == "__main__":
    main()
