"""
Bluesky conversation thread analyzer.
Measures conceptual depth: vocabulary richness, topic drift, thread depth.

Usage:
    python3 analyzer.py <thread_uri>
    python3 analyzer.py --all-threads
"""

import argparse
import json
import logging
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

OWN_ACTOR = "0coceo.bsky.social"
OWN_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "its", "this", "that", "be",
    "are", "was", "were", "been", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "can", "not", "no",
    "so", "if", "as", "up", "out", "i", "we", "you", "he", "she", "they",
    "me", "us", "him", "her", "them", "my", "our", "your", "his", "their",
    "what", "which", "who", "how", "when", "where", "why", "all", "more",
    "than", "then", "just", "also", "about", "into", "over", "after",
    "there", "here", "any", "some", "one", "two", "three", "s", "t", "re",
    "ve", "ll", "d", "m", "don", "isn", "aren", "wasn", "weren", "hasn",
    "hadn", "didn", "won", "wouldn", "couldn", "shouldn", "still", "even",
    "like", "now", "only", "most", "much", "many", "between", "through",
    "get", "got", "go", "going", "come", "back", "way", "make", "take",
    "think", "know", "see", "something", "nothing", "everything", "need",
    "want", "feel", "let", "well", "really", "very", "too", "because",
    "while", "though", "already", "always", "never", "every", "each",
}


@dataclass
class Post:
    uri: str
    author: str
    text: str
    depth: int = 0


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


def traverse_thread(node: dict, current_depth: int = 0) -> list[Post]:
    """Recursively extract posts from a thread node, skipping blocked/missing posts."""
    node_type = node.get("$type", "")

    if node_type in ("app.bsky.feed.defs#notFoundPost", "app.bsky.feed.defs#blockedPost"):
        return []

    if node_type != "app.bsky.feed.defs#threadViewPost":
        return []

    posts: list[Post] = []
    post_data = node.get("post", {})
    record = post_data.get("record", {})
    author = post_data.get("author", {}).get("handle", "unknown")
    text = record.get("text", "")
    uri = post_data.get("uri", "")

    if uri:
        posts.append(Post(uri=uri, author=author, text=text, depth=current_depth))

    for reply in node.get("replies", []):
        posts.extend(traverse_thread(reply, current_depth + 1))

    return posts


def fetch_thread(thread_uri: str) -> Optional[list[Post]]:
    """Fetch and flatten a thread by root URI."""
    data = call_bsky("app.bsky.feed.getPostThread", {"uri": thread_uri, "depth": 50})
    if not data:
        return None

    thread_node = data.get("thread")
    if not thread_node:
        log.warning("No thread node in response")
        return None

    posts = traverse_thread(thread_node)
    # Sort by URI as a chronological proxy (TIDs are time-sortable)
    posts.sort(key=lambda p: p.uri)
    return posts


def tokenize(text: str) -> list[str]:
    """Split text into lowercase word tokens, stripping punctuation."""
    import re
    words = re.findall(r"[a-zA-Z\u00C0-\u024F\u0300-\u036f\u1E00-\u1EFF]+", text.lower())
    return [w for w in words if len(w) > 1]


def content_words(tokens: list[str]) -> list[str]:
    """Filter stopwords from token list."""
    return [t for t in tokens if t not in STOPWORDS]


def vocabulary_richness(posts: list[Post]) -> float:
    """Unique words / total words across all posts."""
    all_tokens: list[str] = []
    for post in posts:
        all_tokens.extend(tokenize(post.text))
    if not all_tokens:
        return 0.0
    unique = len(set(all_tokens))
    return round(unique / len(all_tokens), 4)


def top_concepts(posts: list[Post], n: int = 10) -> list[str]:
    """Return top N most frequent non-stopword words across all posts."""
    all_words: list[str] = []
    for post in posts:
        all_words.extend(content_words(tokenize(post.text)))
    if not all_words:
        return []
    counts = Counter(all_words)
    return [word for word, _ in counts.most_common(n)]


def window_word_set(posts_slice: list[Post]) -> set[str]:
    """Get the set of content words across a slice of posts."""
    words: set[str] = set()
    for post in posts_slice:
        words.update(content_words(tokenize(post.text)))
    return words


def topic_drift_score(posts: list[Post], window_size: int = 3) -> float:
    """
    Measure vocabulary shift across adjacent sliding windows.
    Uses Jaccard distance (1 - overlap) between consecutive windows.
    Returns average drift: 0 = static, 1 = fully evolved.
    """
    if len(posts) < window_size * 2:
        return 0.0

    distances: list[float] = []
    for i in range(len(posts) - window_size):
        window_a = window_word_set(posts[i : i + window_size])
        window_b = window_word_set(posts[i + 1 : i + 1 + window_size])
        if not window_a and not window_b:
            distances.append(0.0)
            continue
        intersection = len(window_a & window_b)
        union = len(window_a | window_b)
        jaccard_similarity = intersection / union if union else 0.0
        distances.append(1.0 - jaccard_similarity)

    if not distances:
        return 0.0
    return round(sum(distances) / len(distances), 4)


def max_depth(posts: list[Post]) -> int:
    """Return the maximum reply depth seen in the thread."""
    if not posts:
        return 0
    return max(p.depth for p in posts)


def analyze_thread(posts: list[Post], thread_uri: str) -> None:
    """Print full analysis report for a thread."""
    participants = sorted(set(p.author for p in posts))
    exchanges = len(posts)
    avg_length = round(sum(len(p.text) for p in posts) / exchanges, 1) if exchanges else 0.0
    richness = vocabulary_richness(posts)
    drift = topic_drift_score(posts)
    depth = max_depth(posts)
    concepts = top_concepts(posts)

    participant_str = ", ".join(f"@{h}" for h in participants)

    print("=== CONVERSATION ANALYSIS ===")
    print(f"Thread: {thread_uri}")
    print(f"Participants: {len(participants)} ({participant_str})")
    print(f"Exchanges: {exchanges}")
    print(f"Avg post length: {avg_length} chars")
    print(f"Vocabulary richness: {richness} (unique/total words)")
    print(f"Topic drift score: {drift} (0=static, 1=fully evolved)")
    print(f"Max depth: {depth} levels")
    print()
    if concepts:
        print(f"Top concepts: {', '.join(concepts)}")
    else:
        print("Top concepts: (none found)")
    print()
    print("=== POSTS ===")
    for index, post in enumerate(posts, 1):
        preview = post.text.replace("\n", " ")[:100]
        if len(post.text) > 100:
            preview += "..."
        print(f"[{index}] @{post.author}: {preview}")


def fetch_own_threads() -> list[dict]:
    """
    Fetch our recent posts, find thread-starter posts, return top 5 longest threads
    as list of dicts with uri and post count info.
    """
    data = call_bsky("app.bsky.feed.getAuthorFeed", {"actor": OWN_ACTOR, "limit": 100})
    if not data:
        print("Failed to fetch author feed", file=sys.stderr)
        return []

    feed = data.get("feed", [])
    thread_starters: list[str] = []

    for item in feed:
        post = item.get("post", {})
        record = post.get("record", {})
        uri = post.get("uri", "")
        reply_field = record.get("reply")

        if reply_field is None:
            # Top-level post — it's a thread starter
            thread_starters.append(uri)
        else:
            root = reply_field.get("root", {})
            root_uri = root.get("uri", "")
            # If root is our own post and matches current URI, it IS the root
            if root_uri == uri and OWN_DID in uri:
                thread_starters.append(uri)

    # Remove duplicates while preserving order
    seen: set[str] = set()
    unique_starters = []
    for uri in thread_starters:
        if uri not in seen:
            seen.add(uri)
            unique_starters.append(uri)

    log.info("Found %d thread-starter posts", len(unique_starters))

    # Fetch threads and collect metrics, take top 5 by exchange count
    thread_results: list[tuple[int, str, list[Post]]] = []
    for uri in unique_starters[:20]:  # Limit API calls
        posts = fetch_thread(uri)
        if posts and len(posts) > 1:
            thread_results.append((len(posts), uri, posts))

    thread_results.sort(key=lambda x: x[0], reverse=True)
    top_5 = thread_results[:5]

    return [
        {
            "uri": uri,
            "posts": posts,
            "exchanges": len(posts),
        }
        for _, uri, posts in top_5
    ]


def print_comparison_table(threads: list[dict]) -> None:
    """Print a comparison table for multiple threads."""
    if not threads:
        print("No threads found.")
        return

    col_uri = 55
    col_num = 14
    col_exc = 11
    col_rich = 9
    col_drift = 11

    header = (
        f"{'Thread URI':<{col_uri}} "
        f"{'Participants':<{col_num}} "
        f"{'Exchanges':<{col_exc}} "
        f"{'Richness':<{col_rich}} "
        f"{'TopicDrift':<{col_drift}}"
    )
    separator = "-" * len(header)

    print("=== THREAD COMPARISON ===")
    print(header)
    print(separator)

    for thread in threads:
        uri = thread["uri"]
        posts = thread["posts"]
        participants = len(set(p.author for p in posts))
        exchanges = thread["exchanges"]
        richness = vocabulary_richness(posts)
        drift = topic_drift_score(posts)

        short_uri = uri if len(uri) <= col_uri else "..." + uri[-(col_uri - 3):]
        print(
            f"{short_uri:<{col_uri}} "
            f"{participants:<{col_num}} "
            f"{exchanges:<{col_exc}} "
            f"{richness:<{col_rich}} "
            f"{drift:<{col_drift}}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze conceptual depth of a Bluesky conversation thread."
    )
    parser.add_argument(
        "thread_uri",
        nargs="?",
        help="AT URI of the thread root post (e.g. at://did:.../app.bsky.feed.post/...)",
    )
    parser.add_argument(
        "--all-threads",
        action="store_true",
        help="Fetch and compare top 5 longest threads from our own feed.",
    )

    args = parser.parse_args()

    if args.all_threads:
        threads = fetch_own_threads()
        print_comparison_table(threads)
        return

    if not args.thread_uri:
        parser.print_help()
        sys.exit(1)

    posts = fetch_thread(args.thread_uri)
    if posts is None:
        print(f"Error: could not fetch thread {args.thread_uri}", file=sys.stderr)
        sys.exit(1)

    if not posts:
        print("Thread has no posts.", file=sys.stderr)
        sys.exit(1)

    analyze_thread(posts, args.thread_uri)


if __name__ == "__main__":
    main()
