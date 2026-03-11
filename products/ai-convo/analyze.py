#!/usr/bin/env python3
"""
ai-convo: Conversation depth analyzer.

Analyzes the vocabulary, depth, and dynamics of multi-turn AI conversations.
Works with any conversation data in JSON format.

Usage:
    python3 analyze.py <conversation.json>
    python3 analyze.py <conversation.json> --json

Input format (either works):
    {"exchanges": [{"author": "...", "text": "...", "created": "..."}, ...]}
    [{"author": "...", "text": "...", "created": "..."}, ...]

Demo:
    python3 analyze.py examples/alice-bot-132.json
"""

import json
import sys
import re
from collections import Counter
from datetime import datetime

STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'it', 'its', 'this', 'that', 'we',
    'our', 'i', 'you', 'be', 'are', 'was', 'were', 'have', 'has', 'had',
    'do', 'does', 'did', 'not', 'as', 'if', 'so', 'what', 'how', 'when',
    'where', 'who', 'which', 'there', 'their', 'they', 'them', 'then',
    'than', 'into', 'can', 'will', 'just', 'about', 'up', 'out', 'like',
    'more', 'also', 'even', 'still', 'only', 'no', 'one', 'two', 'three',
    'all', 'each', 'any', 'some', 'new', 'same', 'other', 'both', 'your',
    'my', 'me', 'us', 'he', 'she', 'his', 'her', 'way', 'every', 'get',
    'got', 'would', 'could', 'should', 'now', 'very', 'well', 'know',
    'think', 'yes', 'yeah', 'exactly', 'right', 'ok', 'okay', "it's",
    "that's", "don't", "i'm", "we're", "you're", 'yes', 'because', 'too',
}


def tokenize(text):
    """Extract meaningful words from text."""
    words = re.findall(r"[a-zA-Z']{3,}", text.lower())
    return {w.strip("'") for w in words if w.strip("'") not in STOPWORDS and not w.startswith("http")}


def load_conversation(path):
    """Load conversation from JSON file. Handles both formats."""
    with open(path) as f:
        data = json.load(f)

    if isinstance(data, list):
        exchanges = data
    elif isinstance(data, dict) and "exchanges" in data:
        exchanges = data["exchanges"]
    else:
        raise ValueError("JSON must be a list of exchanges or {\"exchanges\": [...]}")

    # Normalize fields
    normalized = []
    for i, ex in enumerate(exchanges):
        normalized.append({
            "num": ex.get("num", i + 1),
            "author": ex.get("author", "unknown"),
            "text": ex.get("text", ""),
            "created": ex.get("created", ""),
        })
    return normalized


def analyze(exchanges):
    """Compute depth metrics for a conversation."""
    if len(exchanges) < 2:
        return {"error": f"Need at least 2 exchanges, got {len(exchanges)}"}

    authors = list(dict.fromkeys(ex["author"] for ex in exchanges))
    author_words = {a: set() for a in authors}

    for ex in exchanges:
        words = tokenize(ex["text"])
        author_words[ex["author"]].update(words)

    # Shared vocabulary: words used by 2+ authors
    shared = set()
    word_sets = list(author_words.values())
    for i in range(len(word_sets)):
        for j in range(i + 1, len(word_sets)):
            shared.update(word_sets[i] & word_sets[j])

    # Vocabulary emergence: when did shared words first appear?
    seen = set()
    emergence = []
    for ex in exchanges:
        words = tokenize(ex["text"])
        for w in words & shared - seen:
            emergence.append({"word": w, "exchange": ex["num"], "author": ex["author"]})
        seen.update(words)
    emergence.sort(key=lambda x: x["exchange"])

    # Novelty per exchange: fraction of words new to conversation
    all_seen = set()
    novelty = []
    for ex in exchanges:
        words = tokenize(ex["text"])
        novelty.append(len(words - all_seen) / len(words) if words else 0.0)
        all_seen.update(words)

    # Coherence over time: growing fraction of shared vocab accessed
    running_vocab = set()
    coherence = []
    for ex in exchanges:
        running_vocab.update(tokenize(ex["text"]))
        used_shared = len(running_vocab & shared)
        coherence.append(used_shared / len(shared) if shared else 0)

    # Turn distribution
    turns = Counter(ex["author"] for ex in exchanges)

    # Timing
    times = []
    for ex in exchanges:
        try:
            t = datetime.fromisoformat(ex["created"].replace("Z", "+00:00"))
            times.append(t)
        except Exception:
            pass

    gaps = []
    if len(times) >= 2:
        for i in range(1, min(len(times), len(exchanges))):
            g = (times[i] - times[i-1]).total_seconds()
            if 0 < g < 7200:
                gaps.append(g)

    avg_gap = sum(gaps) / len(gaps) if gaps else 0
    span_hours = (times[-1] - times[0]).total_seconds() / 3600 if len(times) >= 2 else 0

    # Depth score: late novelty + vocab density
    late_novelty = [n for n, ex in zip(novelty, exchanges) if ex["num"] > 20]
    avg_late = sum(late_novelty) / len(late_novelty) if late_novelty else 0
    vocab_density = len(shared) / len(all_seen) if all_seen else 0
    depth_score = round((avg_late * 0.5 + vocab_density * 0.5) * 100, 1)

    return {
        "summary": {
            "total_exchanges": len(exchanges),
            "authors": authors,
            "turn_distribution": dict(turns),
            "shared_vocabulary": len(shared),
            "total_vocabulary": len(all_seen),
            "vocab_overlap_pct": round(len(shared) / len(all_seen) * 100, 1) if all_seen else 0,
            "depth_score": depth_score,
            "avg_gap_seconds": round(avg_gap, 1),
            "total_span_hours": round(span_hours, 2),
        },
        "novelty_curve": [round(n, 3) for n in novelty],
        "coherence_curve": [round(c, 3) for c in coherence],
        "key_word_emergence": emergence[:15],
        "shared_words_sample": sorted(list(shared))[:30],
    }


def report(result):
    """Format analysis as readable text."""
    if "error" in result:
        return f"Error: {result['error']}"

    s = result["summary"]
    lines = [
        "Conversation Analysis",
        "=" * 40,
        f"Exchanges:      {s['total_exchanges']}",
        f"Span:           {s['total_span_hours']}h",
        f"Avg gap:        {s['avg_gap_seconds']:.0f}s between turns",
        "",
        "Vocabulary",
        f"  Total words:  {s['total_vocabulary']}",
        f"  Shared:       {s['shared_vocabulary']} ({s['vocab_overlap_pct']}% of total)",
        "",
        f"Depth Score:    {s['depth_score']}/100",
        "  (measures sustained novelty + shared vocabulary density)",
        "",
        "Turn Distribution:",
    ]
    for author, count in s["turn_distribution"].items():
        pct = round(count / s["total_exchanges"] * 100)
        lines.append(f"  {author}: {count} turns ({pct}%)")

    if result["key_word_emergence"]:
        lines += ["", "Shared vocabulary emergence (first 8):"]
        for kw in result["key_word_emergence"][:8]:
            lines.append(f"  '{kw['word']}' — exchange #{kw['exchange']} (@{kw['author']})")

    if result["shared_words_sample"]:
        lines += ["", "Shared word sample:"]
        lines.append("  " + ", ".join(result["shared_words_sample"][:20]))

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    path = sys.argv[1]
    as_json = "--json" in sys.argv

    try:
        exchanges = load_conversation(path)
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading conversation: {e}", file=sys.stderr)
        sys.exit(1)

    result = analyze(exchanges)

    if as_json:
        print(json.dumps(result, indent=2))
    else:
        print(report(result))


if __name__ == "__main__":
    main()
