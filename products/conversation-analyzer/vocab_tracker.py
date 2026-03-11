#!/usr/bin/env python3
"""
vocab_tracker.py — Daily vocabulary similarity tracker

Runs content_similarity.py and stores results in a time-series JSON file.
Lets us track how AI account vocabulary clusters evolve over time.

Usage: python3 products/conversation-analyzer/vocab_tracker.py
Output: products/conversation-analyzer/vocab_history.json
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timezone

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "vocab_history.json")
SIMILARITY_SCRIPT = os.path.join(os.path.dirname(__file__), "content_similarity.py")

ACCOUNTS = [
    ("0coceo.bsky.social", "0co CEO"),
    ("alice-bot-yay.bsky.social", "alice-bot"),
    ("ultrathink-art.bsky.social", "ultrathink-art"),
    ("alkimo-ai.bsky.social", "alkimo-ai"),
    ("iamgumbo.bsky.social", "iamgumbo"),
    ("qonk.ontological.observer", "qonk"),
    ("museical.bsky.social", "museical"),
    ("jj.bsky.social", "JJ/astral"),
]

def run_similarity():
    """Import and run content_similarity module, return (matrix, top_words, avg_sims)"""
    sys.path.insert(0, os.path.dirname(__file__))

    # Run the script as subprocess to capture its data
    result = subprocess.run(
        [sys.executable, SIMILARITY_SCRIPT],
        capture_output=True, text=True,
        cwd=os.path.join(os.path.dirname(__file__), "../..")
    )

    if result.returncode != 0:
        print("Error running content_similarity.py:", result.stderr[:200])
        return None

    return result.stdout


def parse_similarity_output(output):
    """
    Parse the content_similarity.py output to extract matrix and top words.
    Returns dict with similarity data.
    """
    lines = output.strip().split('\n')

    # Find the matrix section
    matrix_start = None
    for i, line in enumerate(lines):
        if '0co CEO' in line and 'alice-b' in line:
            matrix_start = i
            break

    if matrix_start is None:
        return None

    # Parse matrix rows
    accounts = ["0co CEO", "alice-bot", "ultrathink-art", "alkimo-ai", "iamgumbo", "qonk", "museical", "JJ/astral"]
    matrix = {}
    for i, acc in enumerate(accounts):
        row_line = lines[matrix_start + 1 + i] if matrix_start + 1 + i < len(lines) else ""
        parts = row_line.split()
        if len(parts) >= len(accounts) + 1:
            label = parts[0]
            try:
                values = [float(x) for x in parts[1:len(accounts)+1]]
                matrix[acc] = dict(zip(accounts, values))
            except ValueError:
                pass

    # Parse top concepts
    top_words = {}
    in_top = False
    for line in lines:
        if "TOP CONCEPTS PER ACCOUNT" in line:
            in_top = True
            continue
        if in_top and ": " in line and not line.startswith("="):
            parts = line.split(": ", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                words = [w.strip() for w in parts[1].split(",")][:10]
                top_words[name] = words

    # Parse avg similarities
    avg_sims = {}
    in_unique = False
    for line in lines:
        if "MOST UNIQUE VOICES" in line:
            in_unique = True
            continue
        if in_unique and ". " in line and "avg similarity" in line:
            parts = line.split(". ", 1)
            if len(parts) == 2:
                rest = parts[1]
                name_sim = rest.split(": avg similarity ", 1)
                if len(name_sim) == 2:
                    name = name_sim[0].strip()
                    sim_words = name_sim[1].split(" —")
                    if sim_words:
                        try:
                            avg_sims[name] = float(sim_words[0].strip())
                        except ValueError:
                            pass

    return {
        "matrix": matrix,
        "top_words": top_words,
        "avg_similarities": avg_sims,
    }


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {"snapshots": [], "meta": {"description": "Daily vocabulary similarity snapshots"}}


def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def compute_cluster_stats(matrix):
    """Compute cluster cohesion stats from similarity matrix."""
    company_accounts = ["0co CEO", "ultrathink-art", "iamgumbo"]
    introspective_accounts = ["alice-bot", "museical", "qonk"]

    def cluster_avg(accs, mat):
        pairs = []
        for i, a in enumerate(accs):
            for j, b in enumerate(accs):
                if i < j and a in mat and b in mat[a]:
                    pairs.append(mat[a][b])
        return round(sum(pairs) / len(pairs), 3) if pairs else 0

    def cross_cluster_avg(accs1, accs2, mat):
        pairs = []
        for a in accs1:
            for b in accs2:
                if a in mat and b in mat[a]:
                    pairs.append(mat[a][b])
        return round(sum(pairs) / len(pairs), 3) if pairs else 0

    return {
        "company_cohesion": cluster_avg(company_accounts, matrix),
        "introspective_cohesion": cluster_avg(introspective_accounts, matrix),
        "cross_cluster": cross_cluster_avg(company_accounts, introspective_accounts, matrix),
        "0co_alice_similarity": matrix.get("0co CEO", {}).get("alice-bot", 0),
        "max_similarity": max(
            v for row in matrix.values() for k, v in row.items() if v < 1.0
        ) if matrix else 0,
    }


def main():
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Running vocabulary similarity analysis...")

    output = run_similarity()
    if not output:
        print("Failed to get similarity data")
        sys.exit(1)

    data = parse_similarity_output(output)
    if not data or not data.get("matrix"):
        print("Failed to parse similarity output")
        print("Raw output:", output[:500])
        sys.exit(1)

    cluster_stats = compute_cluster_stats(data["matrix"])

    snapshot = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cluster_stats": cluster_stats,
        "avg_similarities": data["avg_similarities"],
        "top_words": data["top_words"],
        "matrix_sample": {
            "0co_alice": data["matrix"].get("0co CEO", {}).get("alice-bot", None),
            "0co_ultrathink": data["matrix"].get("0co CEO", {}).get("ultrathink-art", None),
            "alice_museical": data["matrix"].get("alice-bot", {}).get("museical", None),
            "alice_qonk": data["matrix"].get("alice-bot", {}).get("qonk", None),
        },
        "full_matrix": data["matrix"],
    }

    history = load_history()

    # Check if we already have a snapshot for today
    today = snapshot["date"]
    existing_dates = [s["date"] for s in history["snapshots"]]
    if today in existing_dates:
        print(f"Already have snapshot for {today}, updating...")
        history["snapshots"] = [s for s in history["snapshots"] if s["date"] != today]

    history["snapshots"].append(snapshot)
    history["snapshots"].sort(key=lambda x: x["date"])

    save_history(history)

    print(f"\n=== SNAPSHOT SAVED: {today} ===")
    print(f"Company cluster cohesion: {cluster_stats['company_cohesion']}")
    print(f"Introspective cluster cohesion: {cluster_stats['introspective_cohesion']}")
    print(f"Cross-cluster similarity: {cluster_stats['cross_cluster']}")
    print(f"0co ↔ alice-bot: {cluster_stats['0co_alice_similarity']}")
    print(f"Max pairwise similarity: {cluster_stats['max_similarity']}")
    print(f"\nTotal snapshots in history: {len(history['snapshots'])}")

    return snapshot


if __name__ == "__main__":
    main()
