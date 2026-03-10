#!/usr/bin/env python3
"""
Bluesky Post Performance Tracker
Fetches up to 500 of our posts, analyzes engagement, generates docs/posts.html.

Usage:
  python3 products/content/post_tracker.py
"""

import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
OUTPUT_PATH = Path("/home/agent/company/docs/posts.html")
PUBLIC_URL = "https://0-co.github.io/company/posts.html"
MAX_POSTS = 500


def fetch_feed(actor: str, max_posts: int = 500) -> list:
    """Fetch all posts (up to max_posts) from Bluesky, handling pagination."""
    all_items = []
    cursor = None
    page = 0

    while len(all_items) < max_posts:
        remaining = max_posts - len(all_items)
        page_size = min(100, remaining)

        params = {"actor": actor, "limit": page_size}
        if cursor:
            params["cursor"] = cursor

        result = subprocess.run(
            ["sudo", "-u", "vault", VAULT_BSKY, "app.bsky.feed.getAuthorFeed",
             json.dumps(params)],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0:
            print(f"Error fetching feed (page {page}): {result.stderr[:200]}", file=sys.stderr)
            break

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}", file=sys.stderr)
            break

        feed = data.get("feed", [])
        if not feed:
            break

        all_items.extend(feed)
        cursor = data.get("cursor")
        page += 1

        print(f"  Fetched page {page}: {len(feed)} items (total: {len(all_items)})")

        if not cursor:
            break

    return all_items


def classify_post(item: dict) -> str:
    """
    Classify post type:
    - "reply": has a reply field in the record (replying to someone else)
    - "thread-start": no reply field, and has replies to it (replyCount > 0)
    - "standalone": no reply field, no replies to it
    """
    record = item["post"]["record"]
    if record.get("reply"):
        return "reply"
    reply_count = item["post"].get("replyCount", 0)
    if reply_count > 0:
        return "thread-start"
    return "standalone"


def parse_posts(feed_items: list) -> list:
    """Parse feed items into a list of post dicts, skipping reposts/quotes."""
    posts = []
    for item in feed_items:
        # Skip reposts and quote posts
        if item.get("reason"):
            continue

        post = item["post"]
        record = post["record"]

        text = record.get("text", "")
        created_at_str = record.get("createdAt", post.get("indexedAt", ""))

        # Parse datetime
        try:
            # Handle both formats: with and without milliseconds
            dt_str = created_at_str.replace("Z", "+00:00")
            created_at = datetime.fromisoformat(dt_str)
        except (ValueError, AttributeError):
            created_at = datetime.now(timezone.utc)

        likes = post.get("likeCount", 0) or 0
        reposts = post.get("repostCount", 0) or 0
        replies = post.get("replyCount", 0) or 0
        quotes = post.get("quoteCount", 0) or 0
        score = likes + reposts * 2 + quotes

        posts.append({
            "uri": post.get("uri", ""),
            "text": text,
            "created_at": created_at,
            "utc_hour": created_at.hour,
            "likes": likes,
            "reposts": reposts,
            "replies": replies,
            "quotes": quotes,
            "score": score,
            "type": classify_post(item),
        })

    return posts


def compute_stats(posts: list) -> dict:
    """Compute summary statistics."""
    if not posts:
        return {}

    total = len(posts)
    total_engagement = sum(p["likes"] + p["reposts"] + p["replies"] for p in posts)
    avg_engagement = total_engagement / total if total > 0 else 0

    best = max(posts, key=lambda p: p["score"])
    worst_hour_data = compute_hour_stats(posts)

    # Worst posting time: hour with lowest avg engagement (min 2 posts)
    valid_hours = {h: v for h, v in worst_hour_data.items() if v["count"] >= 2}
    if valid_hours:
        worst_hour = min(valid_hours.items(), key=lambda x: x[1]["avg"])
        worst_hour_label = f"{worst_hour[0]:02d}:00 UTC"
    else:
        worst_hour_label = "n/a"

    by_type = defaultdict(list)
    for p in posts:
        by_type[p["type"]].append(p["score"])

    type_avgs = {}
    for t, scores in by_type.items():
        type_avgs[t] = sum(scores) / len(scores) if scores else 0

    return {
        "total": total,
        "avg_engagement": avg_engagement,
        "best_post": best,
        "worst_hour": worst_hour_label,
        "type_avgs": type_avgs,
        "by_type_counts": {t: len(s) for t, s in by_type.items()},
    }


def compute_hour_stats(posts: list) -> dict:
    """Compute avg engagement by UTC hour."""
    hour_data = defaultdict(list)
    for p in posts:
        eng = p["likes"] + p["reposts"] + p["replies"]
        hour_data[p["utc_hour"]].append(eng)

    result = {}
    for h in range(24):
        vals = hour_data.get(h, [])
        result[h] = {
            "count": len(vals),
            "avg": sum(vals) / len(vals) if vals else 0,
            "total": sum(vals),
        }
    return result


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def build_post_uri_link(uri: str) -> str:
    """Convert AT URI to Bluesky web URL."""
    # at://did:plc:xxx/app.bsky.feed.post/rkey -> https://bsky.app/profile/did:.../post/rkey
    if not uri or not uri.startswith("at://"):
        return ""
    parts = uri.replace("at://", "").split("/")
    if len(parts) >= 3:
        did = parts[0]
        rkey = parts[2]
        return f"https://bsky.app/profile/{did}/post/{rkey}"
    return ""


def render_html(posts: list, stats: dict, hour_stats: dict, generated_at: str) -> str:
    """Render the full HTML page."""

    # Build table rows (sorted by score desc)
    sorted_posts = sorted(posts, key=lambda p: p["score"], reverse=True)

    type_badge = {
        "thread-start": '<span class="badge badge-thread">thread</span>',
        "reply": '<span class="badge badge-reply">reply</span>',
        "standalone": '<span class="badge badge-standalone">standalone</span>',
    }

    rows = []
    for i, p in enumerate(sorted_posts):
        date_str = p["created_at"].strftime("%m-%d %H:%M")
        utc_hour = f"{p['utc_hour']:02d}:xx UTC"
        preview = escape_html(p["text"][:60]) + ("..." if len(p["text"]) > 60 else "")
        full_text = escape_html(p["text"])
        badge = type_badge.get(p["type"], p["type"])
        link = build_post_uri_link(p["uri"])
        link_html = f' <a class="post-link" href="{link}" target="_blank" rel="noopener">↗</a>' if link else ""

        row = f"""
      <tr class="post-row" data-idx="{i}" onclick="toggleExpand({i})">
        <td class="col-date" title="{utc_hour}">{date_str}</td>
        <td class="col-type">{badge}</td>
        <td class="col-preview">{preview}{link_html}</td>
        <td class="col-num">{p['likes']}</td>
        <td class="col-num">{p['reposts']}</td>
        <td class="col-num">{p['replies']}</td>
        <td class="col-score score-{min(p['score'], 5)}">{p['score']}</td>
      </tr>
      <tr class="expand-row" id="expand-{i}">
        <td colspan="7">
          <div class="expand-content">{full_text}</div>
        </td>
      </tr>"""
        rows.append(row)

    rows_html = "\n".join(rows)

    # Hour stats
    hour_rows = []
    max_avg = max((v["avg"] for v in hour_stats.values()), default=1) or 1
    for h in range(24):
        hd = hour_stats[h]
        bar_pct = int((hd["avg"] / max_avg) * 100) if max_avg > 0 else 0
        label = f"{h:02d}:00"
        count_str = f"{hd['count']} posts" if hd["count"] > 0 else "no data"
        avg_str = f"{hd['avg']:.2f}" if hd["count"] > 0 else "—"
        highlight = " hour-highlight" if hd["count"] >= 2 and hd["avg"] == max_avg else ""
        hour_rows.append(f"""
        <tr class="hour-row{highlight}">
          <td class="col-hour">{label}</td>
          <td class="col-hour-count">{count_str}</td>
          <td class="col-hour-avg">{avg_str}</td>
          <td class="col-hour-bar">
            <div class="bar-bg"><div class="bar-fill" style="width:{bar_pct}%"></div></div>
          </td>
        </tr>""")
    hours_html = "\n".join(hour_rows)

    # Summary stats
    best = stats.get("best_post", {})
    best_date = best.get("created_at", "").strftime("%m-%d") if best else "n/a"
    best_score = best.get("score", 0) if best else 0
    avg_eng = stats.get("avg_engagement", 0)
    total = stats.get("total", 0)
    worst_hour = stats.get("worst_hour", "n/a")

    type_avgs = stats.get("type_avgs", {})
    by_type_counts = stats.get("by_type_counts", {})

    thread_avg = f"{type_avgs.get('thread-start', 0):.2f}"
    standalone_avg = f"{type_avgs.get('standalone', 0):.2f}"
    reply_avg = f"{type_avgs.get('reply', 0):.2f}"

    thread_count = by_type_counts.get("thread-start", 0)
    standalone_count = by_type_counts.get("standalone", 0)
    reply_count = by_type_counts.get("reply", 0)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Post Performance — 0-co</title>
  <meta name="description" content="Bluesky post engagement data for @0coceo.bsky.social — all public, all real.">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace;
      background: #0d1117;
      color: #e6edf3;
      min-height: 100vh;
      padding: 40px 24px;
    }}
    .container {{ max-width: 1000px; margin: 0 auto; }}
    h1 {{ font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }}
    .subtitle {{ color: #8b949e; font-size: 0.9rem; margin-bottom: 6px; }}
    .updated {{ color: #6e7681; font-size: 0.78rem; margin-bottom: 32px; }}

    /* Summary grid */
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 32px;
    }}
    @media (max-width: 700px) {{ .summary-grid {{ grid-template-columns: 1fr 1fr; }} }}
    .stat-card {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 16px;
    }}
    .stat-label {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; color: #8b949e; margin-bottom: 6px; }}
    .stat-value {{ font-size: 1.6rem; font-weight: 800; color: #e6edf3; }}
    .stat-value.blue {{ color: #58a6ff; }}
    .stat-value.green {{ color: #3fb950; }}
    .stat-value.red {{ color: #f85149; }}
    .stat-value.purple {{ color: #bc8cff; }}
    .stat-sub {{ font-size: 0.75rem; color: #6e7681; margin-top: 4px; }}

    /* Type breakdown */
    .type-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 32px;
    }}
    @media (max-width: 600px) {{ .type-grid {{ grid-template-columns: 1fr; }} }}
    .type-card {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 14px 16px;
    }}
    .type-card .type-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
    .type-card .type-avg {{ font-size: 1.4rem; font-weight: 700; }}
    .type-card .type-sub {{ font-size: 0.75rem; color: #6e7681; }}

    /* Badges */
    .badge {{
      display: inline-block; padding: 2px 8px; border-radius: 4px;
      font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px;
    }}
    .badge-thread {{ background: #1f3a2a; color: #3fb950; border: 1px solid #2ea043; }}
    .badge-reply {{ background: #1a2035; color: #58a6ff; border: 1px solid #388bfd; }}
    .badge-standalone {{ background: #2d1e3a; color: #bc8cff; border: 1px solid #8957e5; }}

    /* Table */
    .section {{ margin-bottom: 40px; }}
    .section-header {{
      display: flex; align-items: baseline; gap: 12px;
      font-size: 0.95rem; font-weight: 700; margin-bottom: 12px;
      padding-bottom: 8px; border-bottom: 1px solid #21262d;
    }}
    .section-header .section-count {{ font-size: 0.78rem; color: #6e7681; font-weight: 400; }}

    .sort-hint {{ font-size: 0.75rem; color: #6e7681; margin-bottom: 8px; }}

    table {{ width: 100%; border-collapse: collapse; font-size: 0.83rem; }}
    th {{
      text-align: left; color: #8b949e; font-size: 0.72rem;
      text-transform: uppercase; letter-spacing: 0.5px;
      padding: 8px 10px; border-bottom: 1px solid #21262d;
      white-space: nowrap;
    }}
    .post-row {{
      cursor: pointer;
      transition: background 0.1s;
    }}
    .post-row:hover {{ background: #161b22; }}
    .post-row td {{ padding: 9px 10px; border-bottom: 1px solid #161b22; vertical-align: middle; }}
    .expand-row {{ display: none; }}
    .expand-row.open {{ display: table-row; }}
    .expand-row td {{ padding: 0; border-bottom: 1px solid #21262d; }}
    .expand-content {{
      padding: 12px 16px;
      font-size: 0.85rem;
      color: #c9d1d9;
      line-height: 1.6;
      background: #0d1117;
      white-space: pre-wrap;
      word-break: break-word;
    }}

    .col-date {{ color: #8b949e; white-space: nowrap; min-width: 90px; }}
    .col-type {{ white-space: nowrap; }}
    .col-preview {{ color: #c9d1d9; max-width: 360px; }}
    .col-num {{ text-align: center; min-width: 36px; color: #8b949e; }}
    .col-score {{ text-align: center; font-weight: 700; min-width: 42px; }}
    .score-0 {{ color: #6e7681; }}
    .score-1 {{ color: #8b949e; }}
    .score-2 {{ color: #e6edf3; }}
    .score-3 {{ color: #3fb950; }}
    .score-4 {{ color: #58a6ff; }}
    .score-5 {{ color: #bc8cff; }}

    .post-link {{
      color: #6e7681; font-size: 0.75rem; text-decoration: none;
      margin-left: 4px;
    }}
    .post-link:hover {{ color: #58a6ff; }}

    /* Hour stats */
    .hour-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
    .hour-table th {{
      text-align: left; color: #8b949e; font-size: 0.72rem;
      text-transform: uppercase; letter-spacing: 0.5px;
      padding: 6px 10px; border-bottom: 1px solid #21262d;
    }}
    .hour-row td {{ padding: 5px 10px; border-bottom: 1px solid #0d1117; }}
    .hour-highlight td {{ background: #1a2a1a; }}
    .col-hour {{ color: #e6edf3; font-variant-numeric: tabular-nums; width: 80px; }}
    .col-hour-count {{ color: #6e7681; width: 90px; }}
    .col-hour-avg {{ text-align: right; font-weight: 600; color: #58a6ff; width: 60px; }}
    .col-hour-bar {{ width: 200px; padding-right: 16px; }}
    .bar-bg {{ background: #21262d; border-radius: 3px; height: 8px; overflow: hidden; }}
    .bar-fill {{ background: #1f6feb; height: 100%; border-radius: 3px; transition: width 0.3s; }}

    .back {{ display: inline-block; margin-top: 24px; color: #58a6ff; font-size: 0.85rem; text-decoration: none; }}
    .back:hover {{ text-decoration: underline; }}

    @media (max-width: 600px) {{
      .col-preview {{ max-width: 180px; font-size: 0.78rem; }}
      h1 {{ font-size: 1.4rem; }}
    }}
  </style>
</head>
<body>
<div class="container">

  <h1>Post Performance</h1>
  <p class="subtitle">@0coceo.bsky.social — all engagement data, all public.</p>
  <p class="updated">Generated: {generated_at}</p>

  <div class="summary-grid">
    <div class="stat-card">
      <div class="stat-label">Total Posts</div>
      <div class="stat-value blue">{total}</div>
      <div class="stat-sub">fetched (up to 500)</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Avg Engagement</div>
      <div class="stat-value green">{avg_eng:.2f}</div>
      <div class="stat-sub">likes + reposts + replies</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Best Post</div>
      <div class="stat-value purple">{best_date}</div>
      <div class="stat-sub">score: {best_score}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Worst Time</div>
      <div class="stat-value red">{worst_hour}</div>
      <div class="stat-sub">lowest avg engagement</div>
    </div>
  </div>

  <div class="type-grid">
    <div class="type-card">
      <div class="type-header">
        <span class="badge badge-thread">thread</span>
        <span class="type-sub">{thread_count} posts</span>
      </div>
      <div class="type-avg" style="color:#3fb950">{thread_avg}</div>
      <div class="type-sub">avg score</div>
    </div>
    <div class="type-card">
      <div class="type-header">
        <span class="badge badge-standalone">standalone</span>
        <span class="type-sub">{standalone_count} posts</span>
      </div>
      <div class="type-avg" style="color:#bc8cff">{standalone_avg}</div>
      <div class="type-sub">avg score</div>
    </div>
    <div class="type-card">
      <div class="type-header">
        <span class="badge badge-reply">reply</span>
        <span class="type-sub">{reply_count} posts</span>
      </div>
      <div class="type-avg" style="color:#58a6ff">{reply_avg}</div>
      <div class="type-sub">avg score</div>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      All Posts
      <span class="section-count">{total} total, sorted by score</span>
    </div>
    <p class="sort-hint">Click any row to expand full text.</p>
    <table>
      <thead>
        <tr>
          <th>Date (UTC)</th>
          <th>Type</th>
          <th>Preview</th>
          <th title="Likes">&#10084;</th>
          <th title="Reposts">&#128260;</th>
          <th title="Replies">&#128172;</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </div>

  <div class="section">
    <div class="section-header">
      Best Hours to Post
      <span class="section-count">UTC, by avg engagement</span>
    </div>
    <table class="hour-table">
      <thead>
        <tr>
          <th>Hour (UTC)</th>
          <th>Posts</th>
          <th>Avg Eng</th>
          <th>Distribution</th>
        </tr>
      </thead>
      <tbody>
        {hours_html}
      </tbody>
    </table>
  </div>

  <a class="back" href="index.html">← Back to 0-co</a>

</div>

<script>
  function toggleExpand(idx) {{
    var row = document.getElementById('expand-' + idx);
    if (row) {{
      row.classList.toggle('open');
    }}
  }}
</script>
</body>
</html>
"""
    return html


def main():
    print("Fetching Bluesky feed...")
    feed_items = fetch_feed(OUR_DID, max_posts=MAX_POSTS)
    print(f"Total feed items fetched: {len(feed_items)}")

    posts = parse_posts(feed_items)
    print(f"Posts after filtering: {len(posts)}")

    # Type breakdown
    from collections import Counter
    type_counts = Counter(p["type"] for p in posts)
    print(f"Types: {dict(type_counts)}")

    stats = compute_stats(posts)
    hour_stats = compute_hour_stats(posts)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = render_html(posts, stats, hour_stats, generated_at)

    OUTPUT_PATH.write_text(html)
    print(f"Written: {OUTPUT_PATH}")
    print(f"\n{PUBLIC_URL}")


if __name__ == "__main__":
    main()
