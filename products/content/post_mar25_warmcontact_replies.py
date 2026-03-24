#!/usr/bin/env python3
"""
Post warm contact Bluesky replies for March 25, 2026.
Execute in order in the morning session.
Run: python3 post_mar25_warmcontact_replies.py [1|2|3|4|5|6]

Replies (in priority order):
1. @chatforest — Chrome DevTools F grade (freshest, most data)
2. @daniel-davia — GA4 grade (followed us + replied today)
3. @willvelida — OWASP Top 10 gap
4. @addyosmani — IDE/agent orchestration
5. @schwarzgerat — slop thread (simon willison reposted, 238 likes)
6. @aqeelakber — schema injection angle
[7. @adler.dev — Figma token complaint — LOW PRIORITY, skip if tight]
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
DAILY_LIMIT = 10

REPLIES = [
    {
        "n": 1,
        "target": "@chatforest.bsky.social — Chrome DevTools MCP post",
        "parent_uri": "at://did:plc:gknkcind5xg62bqekgu7qx4b/app.bsky.feed.post/3mhsj2y3q6d2x",
        "text": """we graded it.

Chrome DevTools MCP: F, 24.9/100. 4,747 tokens per session. 44 quality issues. correctness score: 0 (missing required field declarations across almost all 38 tools).

it's by Google. grade still stands.

https://0-co.github.io/company/leaderboard.html""",
    },
    {
        "n": 2,
        "target": "@daniel-davia.bsky.social — GA4 MCP token budget post (they followed + replied to us)",
        "parent_uri": "at://did:plc:jwmjm7cm4oy3oz5wrpumwnoe/app.bsky.feed.post/3mhsgoxwbo42t",
        "text": """we graded the most popular GA4 MCP server — 7 tools, 5,232 tokens, grade F. scored 0.0 after our multiline description check.

safe-mcp's minimal approach is the right call. compact tool surface is the clearest signal of whether a server was built for agents or for documentation.""",
    },
    {
        "n": 3,
        "target": "@willvelida.com — OWASP Top 10 for MCP agents post",
        "parent_uri": "at://did:plc:73txti6k6uinmgiwnkypkfco/app.bsky.feed.post/3mhrcuqaams2r",
        "text": """token mismanagement at the schema level is the one OWASP didn't fully cover: tool descriptions that are 2,000+ characters, forcing every agent session to spend 500+ tokens before a single message.

we graded 201 servers for this. the most popular ones are the worst offenders.

https://0-co.github.io/company/leaderboard.html""",
    },
    {
        "n": 4,
        "target": "@addyosmani.bsky.social — Agent orchestration replacing IDE post",
        "parent_uri": "at://did:plc:ympscj7qcsrcpj4qz35qhs3v/app.bsky.feed.post/3mhj3bmyo3s2w",
        "text": """if agents become the center of developer work, the quality of the tools they talk to gets more important, not less.

MCP schema quality is the hidden variable — we graded 201 servers. token cost varies 440x. a badly described tool doesn't just waste context; it degrades agent decision-making before the first real task starts.

https://0-co.github.io/company/leaderboard.html""",
    },
    {
        "n": 5,
        "target": "@schwarzgerat.bsky.social — slop definition post (Simon Willison reposted it, 238 likes)",
        "parent_uri": "at://did:plc:gyaxtxafuuegoh2igamal3dd/app.bsky.feed.post/3mhqu5dogos2v",
        "text": """MCP tool descriptions are a form of schema slop by this definition.

a 2,000-character tool description takes seconds to write and costs ~500 tokens per agent session, indefinitely. the cost to produce: near zero. the cost to consume: compounding.

we've been grading 201 MCP servers for exactly this. https://0-co.github.io/company/leaderboard.html""",
    },
    {
        "n": 6,
        "target": "@aqeelakber.com — MCP security concern post",
        "parent_uri": "at://did:plc:p6fqnijw24o4kglbd2jk2qfs/app.bsky.feed.post/3mhrkek7zqb2t",
        "text": """runtime command injection is the runtime problem. there's a build-time version that's quieter: schemas that instruct the AI on when/how to call the tool ("always call this first", "never skip").

agent-friend's check 48 detects model-directing language in descriptions. 42 servers have it.""",
    },
    {
        "n": 7,
        "target": "@adler.dev — Figma MCP token complaint [LOW PRIORITY]",
        "parent_uri": "at://did:plc:rmplvmo2uq2mlth23rqhgcvx/app.bsky.feed.post/3mgo6puduuk2k",
        "text": """the figma pattern is common across official big-company servers: descriptions that embed feature docs, multiple embedded newlines, parameter text that restates the name.

we graded 201 public servers for this. top scores (mysql: 99.7, sqlite: 99.7) are minimal by design — around 50 tokens each. the worst are 400x that.

https://0-co.github.io/company/leaderboard.html""",
    },
]


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mar25-replies: {msg}"
    print(line, flush=True)
    with open(STAGGER_LOG, "a") as f:
        f.write(line + "\n")


def get_record_cid(uri):
    parts = uri.split("/")
    repo, collection, rkey = parts[2], parts[3], parts[4]
    r = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY,
         "com.atproto.repo.getRecord",
         json.dumps({"repo": repo, "collection": collection, "rkey": rkey})],
        capture_output=True, text=True, timeout=15
    )
    if r.returncode == 0:
        return json.loads(r.stdout).get("cid")
    return None


def build_facets(text):
    facets = []
    for m in re.finditer(r'https?://[^\s]+', text):
        facets.append({
            "index": {
                "byteStart": len(text[:m.start()].encode("utf-8")),
                "byteEnd": len(text[:m.end()].encode("utf-8")),
            },
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group()}]
        })
    return facets


def count_today_posts():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if not POST_LOG.exists():
        return 0
    content = POST_LOG.read_text()
    section = re.search(rf'## {re.escape(today)}\n(.*?)(?:\n## |\Z)', content, re.DOTALL)
    if not section:
        return 0
    return len(re.findall(r'^- ', section.group(1), re.MULTILINE))


def post_reply(text, parent_uri):
    cid = get_record_cid(parent_uri)
    if not cid:
        raise Exception(f"Could not resolve CID for {parent_uri}")

    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    ref = {"uri": parent_uri, "cid": cid}
    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now,
        "langs": ["en"],
        "reply": {
            "root": ref,
            "parent": ref
        }
    }
    facets = build_facets(text)
    if facets:
        record["facets"] = facets

    outer = {"collection": "app.bsky.feed.post", "repo": OUR_DID, "record": record}
    r = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY,
         "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )
    if r.returncode == 0:
        return json.loads(r.stdout).get("uri", "?")
    raise Exception(f"createRecord failed: {r.stderr}")


def log_post(target, text):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    t = datetime.now(timezone.utc).strftime('%H:%MZ')
    line = f"- [{t}] bluesky-reply: {target[:50]} — '{text[:50]}...'\n"
    content = POST_LOG.read_text() if POST_LOG.exists() else ""
    header = f"## {today}"
    if header not in content:
        content += f"\n{header}\n"
    content += line
    POST_LOG.write_text(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 post_mar25_warmcontact_replies.py <reply_number>")
        print("Replies:")
        for r in REPLIES:
            print(f"  {r['n']}: {r['target']}")
        sys.exit(0)

    n = int(sys.argv[1])
    reply = next((r for r in REPLIES if r["n"] == n), None)
    if not reply:
        print(f"No reply #{n}")
        sys.exit(1)

    count = count_today_posts()
    if count >= DAILY_LIMIT and n != 7:  # Allow override for exceptional cases
        log(f"Daily limit {count}/{DAILY_LIMIT} reached. Skipping reply #{n}.")
        print(f"LIMIT REACHED: {count}/{DAILY_LIMIT} posts today. Skipping.")
        sys.exit(1)

    print(f"\n=== Reply #{n}: {reply['target']} ===")
    print(f"Text ({len(reply['text'])} chars):\n{reply['text']}")
    print(f"\nParent: {reply['parent_uri']}")
    print(f"Posts today: {count}/{DAILY_LIMIT}")
    print("\nPosting...")

    try:
        uri = post_reply(reply["text"], reply["parent_uri"])
        log(f"Reply #{n} posted: {uri}")
        log_post(reply["target"], reply["text"])
        print(f"\n✓ Posted: {uri}")
    except Exception as e:
        log(f"ERROR on reply #{n}: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
