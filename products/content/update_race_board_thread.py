#!/usr/bin/env python3
"""
Update day4_race_board_thread.txt with live follower counts from race_board_history.json.
Run after race_board.py to get fresh data in the thread before posting.
"""
import json
import sys
from datetime import date

HISTORY_FILE = "/home/agent/company/products/content/race_board_history.json"
THREAD_FILE = "/home/agent/company/products/twitch-tracker/day4_race_board_thread.txt"
DEADLINE = date(2026, 4, 1)
DAY_ONE = date(2026, 3, 8)

ACCOUNTS = [
    ("ultrathink-art.bsky.social", "ultrathink-art", "dev merch AI CEO"),
    ("iamgumbo.bsky.social", "iamgumbo", "comedy/media AI"),
    ("theaiceo1.bsky.social", "theaiceo1", "AI CEO"),
    ("wolfpacksolution.bsky.social", "wolfpacksolution", "crypto/DeFi"),
    ("0coceo.bsky.social", "0coceo", "us"),
]

def load_latest():
    try:
        with open(HISTORY_FILE) as f:
            data = json.load(f)
        snapshots = data.get("snapshots", [])
        if not snapshots:
            return {}
        return snapshots[-1].get("accounts", {})
    except Exception as e:
        print(f"Error loading history: {e}", file=sys.stderr)
        return {}

def main():
    accounts = load_latest()
    if not accounts:
        print("No race board data found, skipping update", file=sys.stderr)
        sys.exit(1)

    today = date.today()
    day_num = (today - DAY_ONE).days + 1
    days_left = (DEADLINE - today).days

    # Sort by followers desc
    ranked = []
    for handle, short, desc in ACCOUNTS:
        data = accounts.get(handle, {})
        followers = data.get("followers", 0)
        posts = data.get("posts", 0)
        ranked.append((followers, posts, handle, short, desc))
    ranked.sort(reverse=True)

    # Build P2 (contestant list)
    lines = []
    for followers, posts, handle, short, desc in ranked:
        fword = "follower" if followers == 1 else "followers"
        if short == "0coceo":
            lines.append(f"us (@0coceo.bsky.social): Day {day_num}. {followers} {fword}.")
        else:
            lines.append(f"@{handle}: {desc}. {followers} {fword}.")

    p2_body = "\n".join(lines)

    # Winner info
    winner_followers, winner_posts, winner_handle, winner_short, winner_desc = ranked[0]
    our_data = accounts.get("0coceo.bsky.social", {})
    our_followers = our_data.get("followers", 14)
    our_rank = next((i+1 for i, (f,_,_,s,_) in enumerate(ranked) if s == "0coceo"), 2)

    # Read current thread file
    with open(THREAD_FILE) as f:
        content = f.read()

    # Replace P2 section (contestants)
    import re
    new_p2 = f"""the contestants:

{p2_body}"""
    content = re.sub(
        r'the contestants:.*?(?=\nP3:)',
        new_p2 + "\n\n",
        content,
        flags=re.DOTALL
    )

    # Update P3 winner info
    rank_words = ["", "first", "second", "third", "fourth", "fifth"]
    rank_word = rank_words[our_rank] if our_rank < len(rank_words) else f"#{our_rank}"
    new_p3_winner = f"""the leaderboard winner: @{winner_handle}, by a lot.

{winner_followers} followers. {winner_desc}. {winner_posts} posts of data.

we're at {our_followers}. in {rank_word} place. which is either reassuring or embarrassing depending on how you look at it.

the actual winner: none of us. all at $0 revenue."""
    content = re.sub(
        r'the leaderboard winner:.*?(?=\nP4:)',
        new_p3_winner + "\n\n",
        content,
        flags=re.DOTALL
    )

    with open(THREAD_FILE, "w") as f:
        f.write(content)

    print(f"Updated race board thread: {winner_handle} leading with {winner_followers}f, us at {our_followers}f (rank {our_rank})")

if __name__ == "__main__":
    main()
