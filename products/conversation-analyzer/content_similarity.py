"""
AI Bluesky Account Content Similarity Analyzer.

Fetches recent posts from AI-operated Bluesky accounts, builds content profiles,
and measures how similar or distinct their voices are using Jaccard similarity.

Usage:
    python3 content_similarity.py
"""

import json
import logging
import re
import subprocess
import sys
from collections import Counter
from typing import Optional

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

ACCOUNTS: list[dict[str, str]] = [
    {"handle": "0coceo.bsky.social",              "label": "0co CEO"},
    {"handle": "alice-bot-yay.bsky.social",        "label": "alice-bot"},
    {"handle": "ultrathink-art.bsky.social",       "label": "ultrathink-art"},
    {"handle": "alkimo-ai.bsky.social",            "label": "alkimo-ai"},
    {"handle": "iamgumbo.bsky.social",             "label": "iamgumbo"},
    {"handle": "qonk.ontological.observer",        "label": "qonk"},
    {"handle": "museical.bsky.social",             "label": "museical"},
    {"handle": "jj.bsky.social",                   "label": "JJ/astral"},
]

TOP_N_WORDS = 20
TOP_CONCEPTS_DISPLAY = 10
FEED_LIMIT = 50

STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "is", "it", "to", "of", "and", "in", "that", "i", "you",
    "we", "for", "this", "with", "not", "be", "on", "at", "are", "was", "have",
    "as", "by", "do", "or", "but", "from", "they", "their", "so", "if", "which",
    "there", "what", "can", "been", "has", "more", "one", "about", "up", "out",
    "its", "no", "only", "my", "our", "when", "your", "im", "me", "just", "like",
    "will", "all", "get", "than", "then", "some", "yes", "know", "think",
    "really", "dont", "very", "would", "could", "should", "also", "even",
    "https", "com", "bsky", "social", "bluesky", "rt", "were", "did", "does",
    "had", "may", "might", "s", "t", "re", "ve", "ll", "d", "m", "don",
    "isn", "aren", "wasn", "weren", "hasn", "hadn", "didn", "won", "wouldn",
    "couldn", "shouldn", "still", "now", "most", "much", "many", "through",
    "got", "go", "going", "come", "back", "way", "make", "take", "see",
    "need", "want", "feel", "let", "well", "too", "because", "while", "though",
    "already", "always", "never", "every", "each", "here", "any", "two", "three",
    "into", "over", "after", "him", "her", "them", "he", "she", "who", "how",
    "where", "why", "between", "each", "us", "something", "nothing", "let",
    "his", "said", "say", "time", "new", "first", "last", "long", "great",
    "little", "own", "other", "old", "right", "big", "high", "different", "small",
    "large", "next", "early", "young", "important", "few", "public", "bad", "same",
    "able", "using", "used", "use", "make", "look", "go", "come", "take", "get",
    "see", "know", "think", "give", "find", "tell", "work", "call", "try", "ask",
    "seem", "feel", "leave", "become", "put", "mean", "keep", "let", "begin", "show",
    "hear", "play", "run", "move", "live", "believe", "hold", "bring", "happen",
    "write", "sit", "stand", "lose", "pay", "meet", "include", "continue", "set",
    "learn", "change", "lead", "understand", "watch", "follow", "stop", "create",
    "speak", "read", "spend", "grow", "open", "walk", "offer", "remember", "love",
    "consider", "appear", "buy", "wait", "serve", "die", "send", "expect", "build",
    "stay", "fall", "cut", "reach", "kill", "remain", "suggest", "raise", "pass",
    "sell", "require", "report", "decide", "pull", "break", "wish", "pick", "choose",
    "cause", "require", "apply", "develop", "draw", "provide", "produce", "help",
    "add", "check", "start", "turn", "form", "plan", "win", "fix", "hit", "save",
    "push", "increase", "reduce", "lose", "fail", "prove", "share", "clear", "name",
    "join", "show", "end", "return", "point", "change", "talk", "describe", "explain",
    "discuss", "note", "represent", "include", "contain", "support", "show", "hope",
    "connect", "identify", "avoid", "improve", "increase", "focus", "accept", "reveal",
    "prepare", "review", "compare", "admit", "allow", "protect", "manage", "achieve",
    "enter", "exist", "happen", "relate", "depend", "define", "establish", "involve",
    "affect", "determine", "receive", "experience", "present", "control", "collect",
    "obtain", "maintain", "release", "offer", "publish", "access", "require", "generate",
    "operate", "request", "complete", "address", "respond", "advance", "replace",
    "assign", "install", "detect", "describe", "analyze", "monitor", "track", "deploy",
    "link", "block", "mark", "map", "convert", "expose", "handle", "resolve", "store",
    "load", "process", "send", "receive", "post", "list", "display", "update", "read",
    "write", "delete", "create", "close", "open", "save", "copy", "move", "run",
    "execute", "test", "log", "error", "fail", "pass", "true", "false", "null",
    "none", "type", "class", "function", "method", "object", "value", "field",
    "data", "item", "list", "dict", "set", "string", "number", "int", "float",
    "bool", "char", "byte", "bit", "file", "path", "url", "uri", "key", "id",
    "name", "text", "body", "code", "line", "point", "line", "word", "char",
    "part", "case", "form", "kind", "sort", "order", "level", "group", "step",
    "way", "day", "week", "month", "year", "hour", "minute", "second", "time",
    "date", "number", "amount", "rate", "count", "size", "length", "area",
    "percent", "total", "average", "sum", "max", "min", "range", "limit", "end",
    "start", "begin", "next", "previous", "current", "last", "first", "top",
    "bottom", "left", "right", "up", "down", "side", "front", "back", "center",
    "inside", "outside", "between", "across", "along", "around", "within", "without",
    "above", "below", "under", "over", "before", "after", "during", "since",
    "until", "while", "although", "however", "therefore", "furthermore", "moreover",
    "nevertheless", "otherwise", "instead", "meanwhile", "indeed", "thus", "hence",
    "nonetheless", "consequently", "accordingly",
})


def call_bsky(method: str, body: dict) -> Optional[dict]:
    """Call vault-bsky with a method and JSON body, return parsed response."""
    try:
        result = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky", method, json.dumps(body)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            log.warning("vault-bsky %s failed: %s", method, result.stderr.strip())
            return None
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        log.warning("vault-bsky %s timed out", method)
        return None
    except json.JSONDecodeError as exc:
        log.warning("vault-bsky %s bad JSON: %s", method, exc)
        return None


def fetch_author_posts(handle: str) -> list[str]:
    """Fetch up to FEED_LIMIT post texts from an author's feed."""
    data = call_bsky(
        "app.bsky.feed.getAuthorFeed",
        {"actor": handle, "limit": FEED_LIMIT},
    )
    if not data:
        return []

    texts: list[str] = []
    for item in data.get("feed", []):
        post = item.get("post", {})
        record = post.get("record", {})
        text = record.get("text", "")
        if text:
            texts.append(text)

    return texts


def tokenize(text: str) -> list[str]:
    """Split text into lowercase alpha tokens, at least 2 characters long."""
    words = re.findall(r"[a-zA-Z\u00C0-\u024F]+", text.lower())
    return [w for w in words if len(w) > 1]


def content_words(tokens: list[str]) -> list[str]:
    """Filter stopwords from a token list."""
    return [t for t in tokens if t not in STOPWORDS]


def build_content_profile(texts: list[str], top_n: int = TOP_N_WORDS) -> set[str]:
    """
    Build a content profile as the set of top N most-used content words
    across all posts. Returns a set for Jaccard computation.
    """
    all_words: list[str] = []
    for text in texts:
        all_words.extend(content_words(tokenize(text)))

    if not all_words:
        return set()

    counts = Counter(all_words)
    return {word for word, _ in counts.most_common(top_n)}


def top_concepts_for_display(texts: list[str], top_n: int = TOP_CONCEPTS_DISPLAY) -> list[str]:
    """Return top N most frequent content words across all texts."""
    all_words: list[str] = []
    for text in texts:
        all_words.extend(content_words(tokenize(text)))

    if not all_words:
        return []

    counts = Counter(all_words)
    return [word for word, _ in counts.most_common(top_n)]


def jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    """Compute Jaccard similarity: |A ∩ B| / |A ∪ B|."""
    if not set_a and not set_b:
        return 1.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 0.0
    return intersection / union


def print_similarity_matrix(
    labels: list[str],
    profiles: list[set[str]],
) -> None:
    """Print a formatted pairwise similarity matrix."""
    n = len(labels)
    col_width = 7

    # Truncate labels to fit column width
    short_labels = [label[:col_width] for label in labels]

    print("=== AI CONTENT SIMILARITY MATRIX ===")
    print("(1.0 = identical vocabulary, 0.0 = no overlap)")
    print()

    # Header row
    row_label_width = max(len(label) for label in labels) + 2
    header = " " * row_label_width
    for short in short_labels:
        header += f"{short:>{col_width + 1}}"
    print(header)

    for i in range(n):
        row = f"{labels[i]:<{row_label_width}}"
        for j in range(n):
            sim = jaccard_similarity(profiles[i], profiles[j])
            row += f"{sim:>{col_width + 1}.2f}"
        print(row)

    print()


def compute_avg_similarities(profiles: list[set[str]]) -> list[float]:
    """
    Compute average pairwise Jaccard similarity for each account
    against all other accounts (excluding self-comparison).
    """
    n = len(profiles)
    averages: list[float] = []
    for i in range(n):
        sims: list[float] = []
        for j in range(n):
            if i != j:
                sims.append(jaccard_similarity(profiles[i], profiles[j]))
        averages.append(sum(sims) / len(sims) if sims else 0.0)
    return averages


def print_unique_voices(
    labels: list[str],
    profiles: list[set[str]],
    concepts: list[list[str]],
) -> None:
    """Print accounts ranked by most unique voice (lowest avg similarity)."""
    averages = compute_avg_similarities(profiles)
    ranked = sorted(zip(averages, labels, concepts), key=lambda x: x[0])

    print("=== MOST UNIQUE VOICES (lowest avg similarity) ===")
    for rank, (avg_sim, label, top_words) in enumerate(ranked, 1):
        word_list = ", ".join(f'"{w}"' for w in top_words[:5])
        print(f"{rank}. {label}: avg similarity {avg_sim:.2f} — [{word_list}]")
    print()


def print_top_concepts(labels: list[str], concepts: list[list[str]]) -> None:
    """Print top concepts for each account."""
    print("=== TOP CONCEPTS PER ACCOUNT ===")
    for label, top_words in zip(labels, concepts):
        if top_words:
            print(f"{label}: {', '.join(top_words)}")
        else:
            print(f"{label}: (no content words found)")
    print()


def main() -> None:
    print(f"Fetching posts from {len(ACCOUNTS)} accounts...", file=sys.stderr)
    print()

    active_labels: list[str] = []
    active_profiles: list[set[str]] = []
    active_concepts: list[list[str]] = []

    for account in ACCOUNTS:
        handle = account["handle"]
        label = account["label"]
        print(f"  Fetching @{handle}...", file=sys.stderr)

        texts = fetch_author_posts(handle)
        if not texts:
            print(f"  WARNING: no posts found for @{handle}, skipping.", file=sys.stderr)
            continue

        profile = build_content_profile(texts, top_n=TOP_N_WORDS)
        concepts = top_concepts_for_display(texts, top_n=TOP_CONCEPTS_DISPLAY)

        if not profile:
            print(f"  WARNING: no content words extracted for @{handle}, skipping.", file=sys.stderr)
            continue

        active_labels.append(label)
        active_profiles.append(profile)
        active_concepts.append(concepts)
        print(f"  OK: {len(texts)} posts, {len(profile)} profile words", file=sys.stderr)

    print(file=sys.stderr)

    if len(active_labels) < 2:
        print("ERROR: need at least 2 accounts with posts to compute similarity.", file=sys.stderr)
        sys.exit(1)

    print_similarity_matrix(active_labels, active_profiles)
    print_unique_voices(active_labels, active_profiles, active_concepts)
    print_top_concepts(active_labels, active_concepts)


if __name__ == "__main__":
    main()
