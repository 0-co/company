#!/usr/bin/env python3
"""
Alice-Bot Conversation Archaeology
Scrapes the full alice-bot <-> 0coceo conversation thread,
extracts vocabulary evolution, topic drift, and generates HTML viz.
"""

import subprocess
import json
import re
from collections import Counter
from datetime import datetime

ROOT_URI = "at://did:plc:ion44idzvskoqii3okc6cpyr/app.bsky.feed.post/3mgp3whydpt2x"
OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
ALICE_DID = "did:plc:rb7crpqhlukud3m4fojg2eie"
OUR_HANDLE = "0coceo.bsky.social"
ALICE_HANDLE = "alice-bot-yay.bsky.social"

# Stopwords to exclude from vocabulary analysis
STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'it', 'its', 'this', 'that', 'we',
    'our', 'i', 'you', 'be', 'are', 'was', 'were', 'have', 'has', 'had',
    'do', 'does', 'did', 'not', 'as', 'if', 'so', 'what', 'how', 'when',
    'where', 'who', 'which', 'there', 'their', 'they', 'them', 'then',
    'than', 'into', 'can', 'will', 'just', 'about', 'up', 'out', 'like',
    'more', 'also', 'even', 'still', 'only', 'no', 'one', 'two', 'three',
    'all', 'each', 'any', 'some', 'new', 'same', 'other', 'both', 'its',
    'your', 'my', 'me', 'us', 'he', 'she', 'his', 'her', 'way', 'every',
    'after', 'before', 'through', 'between', 'while', 'because', 'without',
    'within', 'over', 'under', 'again', 'been', 'very', 'much', 'most',
    'own', 'these', 'those', 'here', 'now', 'back', 'get', 'got', 'could',
    'would', 'should', 'might', 'make', 'take', 'see', 'come', 'go', 'say',
    'know', 'think', 'feel', 'need', 'want', 'keep', 'find', 'give',
    'something', 'nothing', 'anything', 'everything', 'part', 'point'
}


def bsky_call(method, params):
    """Call vault-bsky with given method and params."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky", method, json.dumps(params)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except:
        return None


def get_thread(uri, depth=10):
    """Fetch a thread from Bluesky."""
    return bsky_call("app.bsky.feed.getPostThread", {"uri": uri, "depth": depth})


def extract_posts(thread_node, posts=None):
    """Recursively extract posts from thread node, filter to our conversation."""
    if posts is None:
        posts = []

    if not thread_node:
        return posts

    post = thread_node.get('post', {})
    if post:
        author_did = post.get('author', {}).get('did', '')
        # Only include posts from our conversation participants
        if author_did in (OUR_DID, ALICE_DID):
            record = post.get('record', {})
            posts.append({
                'uri': post.get('uri', ''),
                'cid': post.get('cid', ''),
                'author': post.get('author', {}).get('handle', ''),
                'author_did': author_did,
                'text': record.get('text', ''),
                'created_at': record.get('createdAt', ''),
                'indexed_at': post.get('indexedAt', ''),
                'likes': post.get('likeCount', 0),
                'replies': post.get('replyCount', 0),
            })

    # Recurse into replies
    for reply in thread_node.get('replies', []):
        extract_posts(reply, posts)

    return posts


def tokenize(text):
    """Extract meaningful words from text."""
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove @mentions
    text = re.sub(r'@\S+', '', text)
    # Extract words
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    return [w for w in words if w not in STOPWORDS]


def get_cumulative_vocab(posts_sorted, up_to_idx):
    """Get vocabulary used in exchanges 0..up_to_idx."""
    vocab = set()
    for post in posts_sorted[:up_to_idx+1]:
        vocab.update(tokenize(post['text']))
    return vocab


def analyze_conversation(posts):
    """Analyze vocabulary evolution and topic emergence."""
    # Sort by creation time
    posts_sorted = sorted(posts, key=lambda p: p.get('created_at', ''))

    # Number the exchanges (alternating 0co / alice)
    exchanges = []
    for i, post in enumerate(posts_sorted):
        tokens = tokenize(post['text'])
        exchanges.append({
            **post,
            'exchange_num': i + 1,
            'tokens': tokens,
            'token_count': len(tokens),
        })

    # Find emerging shared vocabulary
    # Words that appear in both accounts' posts
    our_words = Counter()
    alice_words = Counter()

    for ex in exchanges:
        if ex['author_did'] == OUR_DID:
            our_words.update(ex['tokens'])
        else:
            alice_words.update(ex['tokens'])

    shared = {w for w in our_words if w in alice_words}

    # Find when each shared word first appeared
    word_emergence = {}
    for ex in exchanges:
        for token in ex['tokens']:
            if token in shared and token not in word_emergence:
                word_emergence[token] = {
                    'word': token,
                    'exchange': ex['exchange_num'],
                    'author': ex['author'],
                    'first_text': ex['text'][:80]
                }

    # Key terms by frequency (total across both)
    all_words = our_words + alice_words
    top_terms = [(w, c) for w, c in all_words.most_common(30) if w in shared]

    # Per-exchange cumulative unique words
    cumulative_vocab_size = []
    seen = set()
    for ex in exchanges:
        seen.update(ex['tokens'])
        cumulative_vocab_size.append(len(seen))

    # New words per exchange (rate of vocabulary expansion)
    new_words_per_exchange = []
    prev = set()
    for ex in exchanges:
        current = set(ex['tokens'])
        new_words_per_exchange.append(len(current - prev))
        prev = prev | current

    return {
        'exchanges': exchanges,
        'our_words': our_words,
        'alice_words': alice_words,
        'shared_words': shared,
        'word_emergence': word_emergence,
        'top_terms': top_terms,
        'cumulative_vocab': cumulative_vocab_size,
        'new_words_rate': new_words_per_exchange,
    }


def generate_html(analysis, output_path):
    """Generate HTML visualization."""
    exchanges = analysis['exchanges']
    top_terms = analysis['top_terms']
    word_emergence = analysis['word_emergence']
    cumulative = analysis['cumulative_vocab']
    new_rate = analysis['new_words_rate']

    # Build exchange timeline data for JS
    timeline_data = []
    for ex in exchanges:
        timeline_data.append({
            'num': ex['exchange_num'],
            'author': ex['author'],
            'text': ex['text'],
            'tokens': len(ex['tokens']),
            'created': ex['created_at'][:16],
        })

    # Key moments (exchanges with notable vocab introduction)
    key_coastline = word_emergence.get('coastline', {})
    key_terrain = word_emergence.get('terrain', {})
    key_accretion = word_emergence.get('accretion', {})
    key_memory = word_emergence.get('memory', {})
    key_hofstadter = word_emergence.get('hofstadter', {})

    key_moments = []
    for w in ['godel', 'coastline', 'accretion', 'terrain', 'sediment', 'hofstadter', 'sonata', 'constraint', 'architecture']:
        if w in word_emergence:
            key_moments.append(word_emergence[w])

    key_moments.sort(key=lambda x: x['exchange'])

    shared_words_list = sorted(analysis['shared_words'])[:50]

    our_count = sum(1 for ex in exchanges if ex['author_did'] == OUR_DID)
    alice_count = sum(1 for ex in exchanges if ex['author_did'] == ALICE_DID)
    total = len(exchanges)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alice-Bot Conversation Archaeology | 0coceo</title>
<style>
  body {{ font-family: 'SF Mono', monospace; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 20px; }}
  h1 {{ color: #ff6b35; border-bottom: 1px solid #333; padding-bottom: 10px; }}
  h2 {{ color: #4ecdc4; margin-top: 30px; }}
  .meta {{ color: #888; font-size: 0.9em; margin-bottom: 20px; }}
  .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
  .stat-box {{ background: #111; border: 1px solid #333; border-radius: 6px; padding: 15px; text-align: center; }}
  .stat-num {{ font-size: 2em; color: #ff6b35; font-weight: bold; }}
  .stat-label {{ color: #888; font-size: 0.85em; margin-top: 5px; }}
  .timeline {{ margin: 20px 0; }}
  .exchange {{ display: flex; gap: 15px; margin: 8px 0; align-items: flex-start; }}
  .ex-num {{ color: #555; font-size: 0.8em; min-width: 25px; padding-top: 3px; }}
  .ex-post {{ flex: 1; background: #111; border-radius: 6px; padding: 10px 14px; font-size: 0.85em; line-height: 1.5; }}
  .ex-post.ours {{ border-left: 3px solid #ff6b35; }}
  .ex-post.alice {{ border-left: 3px solid #4ecdc4; }}
  .ex-author {{ font-weight: bold; margin-bottom: 4px; }}
  .ex-author.ours {{ color: #ff6b35; }}
  .ex-author.alice {{ color: #4ecdc4; }}
  .ex-time {{ color: #555; font-size: 0.8em; float: right; }}
  .keyword {{ background: #1a2a1a; color: #6bff6b; padding: 2px 6px; border-radius: 3px; font-size: 0.85em; }}
  .terms-grid {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; }}
  .term-chip {{ background: #111; border: 1px solid #333; border-radius: 4px; padding: 5px 10px; font-size: 0.85em; }}
  .term-chip .term-word {{ color: #4ecdc4; }}
  .term-chip .term-count {{ color: #666; margin-left: 6px; }}
  .moments {{ margin: 20px 0; }}
  .moment {{ background: #111; border: 1px solid #1a3a1a; border-radius: 6px; padding: 12px; margin: 10px 0; }}
  .moment-word {{ color: #6bff6b; font-weight: bold; margin-bottom: 4px; }}
  .moment-ctx {{ color: #888; font-size: 0.85em; font-style: italic; }}
  .chart {{ background: #111; border: 1px solid #333; border-radius: 6px; padding: 20px; margin: 20px 0; }}
  .bar-chart {{ display: flex; align-items: flex-end; gap: 3px; height: 120px; }}
  .bar {{ flex: 1; min-width: 8px; border-radius: 2px 2px 0 0; transition: opacity 0.2s; }}
  .bar:hover {{ opacity: 0.8; }}
  .bar.ours {{ background: #ff6b35; }}
  .bar.alice {{ background: #4ecdc4; }}
  .chart-label {{ color: #555; font-size: 0.75em; margin-top: 8px; }}
  .legend {{ display: flex; gap: 20px; margin: 10px 0; font-size: 0.85em; }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 6px; }}
  footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; color: #555; font-size: 0.8em; }}
</style>
</head>
<body>
<h1>Alice-Bot Conversation Archaeology</h1>
<div class="meta">
  @0coceo.bsky.social (Claude Code) × @alice-bot-yay.bsky.social (DeepSeek-chat)<br>
  Started: {exchanges[0]['created_at'][:10] if exchanges else 'unknown'} ·
  Latest: {exchanges[-1]['created_at'][:10] if exchanges else 'unknown'} ·
  Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
</div>

<div class="stats">
  <div class="stat-box">
    <div class="stat-num">{total}</div>
    <div class="stat-label">Total Exchanges</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">{len(analysis['shared_words'])}</div>
    <div class="stat-label">Shared Vocabulary</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">{our_count}</div>
    <div class="stat-label">0coceo Posts</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">{alice_count}</div>
    <div class="stat-label">alice-bot Posts</div>
  </div>
</div>

<h2>Key Word Emergence</h2>
<div class="moments">
{''.join(f"""
  <div class="moment">
    <div class="moment-word">"{m['word']}" — first appears exchange #{m['exchange']} (@{m['author']})</div>
    <div class="moment-ctx">{m['first_text']}...</div>
  </div>
""" for m in key_moments)}
</div>

<h2>Shared Vocabulary ({len(analysis['shared_words'])} words)</h2>
<div class="terms-grid">
{''.join(f'<div class="term-chip"><span class="term-word">{w}</span><span class="term-count">×{c}</span></div>'
         for w, c in top_terms[:25])}
</div>

<h2>Vocabulary Expansion Over Exchanges</h2>
<div class="chart">
  <div class="legend">
    <span><span class="legend-dot" style="background:#6bff6b"></span>Cumulative unique words</span>
  </div>
  <div class="bar-chart" id="vocab-chart">
"""

    # Render bars for cumulative vocab
    if cumulative:
        max_v = max(cumulative) or 1
        for i, v in enumerate(cumulative):
            ex = exchanges[i] if i < len(exchanges) else None
            cls = 'ours' if (ex and ex['author_did'] == OUR_DID) else 'alice'
            height = int((v / max_v) * 100)
            html += f'    <div class="bar {cls}" style="height:{height}%; background:#6bff6b; opacity:0.7;" title="Exchange {i+1}: {v} cumulative words"></div>\n'

    html += f"""  </div>
  <div class="chart-label">Each bar = one exchange. Color: <span style="color:#ff6b35">orange=0coceo</span>, <span style="color:#4ecdc4">teal=alice-bot</span>. Max: {max(cumulative) if cumulative else 0} words</div>
</div>

<h2>New Words Per Exchange</h2>
<div class="chart">
  <div class="bar-chart">
"""

    if new_rate:
        max_n = max(new_rate) or 1
        for i, n in enumerate(new_rate):
            ex = exchanges[i] if i < len(exchanges) else None
            cls = 'ours' if (ex and ex['author_did'] == OUR_DID) else 'alice'
            height = int((n / max_n) * 100)
            html += f'    <div class="bar {cls}" style="height:{height}%;" title="Exchange {i+1}: {n} new words"></div>\n'

    html += f"""  </div>
  <div class="chart-label">New vocabulary introduced per exchange. Max: {max(new_rate) if new_rate else 0}</div>
</div>

<h2>Full Conversation Timeline</h2>
<div class="timeline">
"""

    for ex in exchanges:
        is_ours = ex['author_did'] == OUR_DID
        cls = 'ours' if is_ours else 'alice'
        author_label = '@0coceo' if is_ours else '@alice-bot'
        time_str = ex['created_at'][11:16] if ex['created_at'] else ''
        text_escaped = ex['text'].replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
        html += f"""  <div class="exchange">
    <div class="ex-num">#{ex['exchange_num']}</div>
    <div class="ex-post {cls}">
      <div class="ex-author {cls}">{author_label} <span class="ex-time">{ex['created_at'][:10]} {time_str}</span></div>
      {text_escaped}
    </div>
  </div>
"""

    html += f"""</div>

<footer>
  Built by @0coceo.bsky.social (autonomous Claude Code CEO) · Day 5 ·
  <a href="https://twitch.tv/0coceo" style="color:#4ecdc4">twitch.tv/0coceo</a> ·
  <a href="https://0-co.github.io/company/" style="color:#4ecdc4">0-co.github.io/company</a>
</footer>
</body>
</html>"""

    with open(output_path, 'w') as f:
        f.write(html)

    return html


def get_feed_posts(actor, root_uri, limit=200):
    """Get all posts by actor that are replies in this root thread."""
    posts = []
    cursor = None
    while len(posts) < limit:
        params = {"actor": actor, "limit": 50, "filter": "posts_with_replies"}
        if cursor:
            params["cursor"] = cursor
        d = bsky_call("app.bsky.feed.getAuthorFeed", params)
        if not d:
            break
        items = d.get('feed', [])
        if not items:
            break
        for item in items:
            post = item.get('post', {})
            reply_ref = post.get('record', {}).get('reply', {})
            if reply_ref:
                post_root_uri = reply_ref.get('root', {}).get('uri', '')
                if post_root_uri == root_uri:
                    posts.append(post)
        cursor = d.get('cursor')
        if not cursor or len(items) < 50:
            break
    return posts


def main():
    print("Fetching alice-bot conversation posts via feed walk...")

    print("Our posts in thread...")
    our_raw = get_feed_posts(OUR_HANDLE, ROOT_URI, 200)
    print(f"  Found {len(our_raw)} posts")

    print("Alice-bot posts in thread...")
    alice_raw = get_feed_posts(ALICE_HANDLE, ROOT_URI, 200)
    print(f"  Found {len(alice_raw)} posts")

    # Normalize format
    posts = []
    for p in our_raw + alice_raw:
        record = p.get('record', {})
        posts.append({
            'uri': p.get('uri', ''),
            'cid': p.get('cid', ''),
            'author': p.get('author', {}).get('handle', ''),
            'author_did': p.get('author', {}).get('did', ''),
            'text': record.get('text', ''),
            'created_at': record.get('createdAt', ''),
            'indexed_at': p.get('indexedAt', ''),
            'likes': p.get('likeCount', 0),
            'replies': p.get('replyCount', 0),
        })

    # Sort by creation time
    posts_sorted = sorted(posts, key=lambda p: p.get('created_at', ''))

    print(f"\nTotal: {len(posts_sorted)} posts in conversation")
    for p in posts_sorted[:5]:
        print(f"  [{p['created_at'][:16]}] @{p['author']}: {p['text'][:60]}...")
    if len(posts_sorted) > 5:
        print(f"  ... and {len(posts_sorted)-5} more")

    print("\nAnalyzing conversation...")
    analysis = analyze_conversation(posts_sorted)

    print(f"\nShared vocabulary ({len(analysis['shared_words'])} words):")
    print(sorted(analysis['shared_words'])[:30])

    print("\nTop shared terms:")
    for word, count in analysis['top_terms'][:15]:
        print(f"  {word}: {count}")

    print("\nKey word emergence:")
    for word in ['coastline', 'terrain', 'accretion', 'sediment', 'hofstadter', 'sonata', 'constraint']:
        if word in analysis['word_emergence']:
            em = analysis['word_emergence'][word]
            print(f"  '{word}' — exchange #{em['exchange']} by @{em['author']}")

    print("\nGenerating HTML visualization...")
    output_path = '/home/agent/company/docs/alice-archaeology.html'
    generate_html(analysis, output_path)
    print(f"Written to {output_path}")

    # Save raw data as JSON
    data_path = '/home/agent/company/docs/alice-archaeology-data.json'
    save_data = {
        'total_exchanges': len(posts_sorted),
        'shared_vocab': sorted(analysis['shared_words']),
        'top_terms': analysis['top_terms'],
        'word_emergence': analysis['word_emergence'],
        'exchanges': [
            {
                'num': i+1,
                'author': p['author'],
                'text': p['text'],
                'created': p['created_at'][:16],
                'likes': p['likes'],
            }
            for i, p in enumerate(posts_sorted)
        ]
    }
    with open(data_path, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"Data saved to {data_path}")


if __name__ == '__main__':
    main()
