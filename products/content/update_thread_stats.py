#!/usr/bin/env python3
"""Update live follower stats in Day 4 thread files before posting."""

import json, re, subprocess, sys
from datetime import date

BROADCASTER_ID = "1455485722"
OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
DEADLINE = date(2026, 4, 1)
DAY_ONE = date(2026, 3, 8)


def get_twitch_followers():
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "GET", f"/channels/followers?broadcaster_id={BROADCASTER_ID}"],
        capture_output=True, text=True
    )
    try:
        return json.loads(r.stdout).get("total", 1)
    except Exception:
        return 1


def get_bsky_followers():
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "app.bsky.actor.getProfile", json.dumps({"actor": OUR_DID})],
        capture_output=True, text=True
    )
    try:
        return json.loads(r.stdout).get("followersCount", 14)
    except Exception:
        return 14


def update_file(path, replacements):
    """replacements: list of (old_str, new_str) tuples"""
    with open(path) as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)


def main():
    twitch_f = get_twitch_followers()
    bsky_f = get_bsky_followers()
    today = date.today()
    day_num = (today - DAY_ONE).days + 1
    days_left = (DEADLINE - today).days

    print(f"Live stats: Twitch={twitch_f}/50, Bluesky={bsky_f}, Day {day_num}, {days_left}d left")

    base = "/home/agent/company/products/twitch-tracker"

    # Update day4_first5min_thread.txt P6
    first5 = f"{base}/day4_first5min_thread.txt"
    # P6 line: "Day 4. 1 Twitch follower. 14 Bluesky followers."
    with open(first5) as f:
        content = f.read()
    # Replace the Day N line with current stats
    new_p6_line = f"Day {day_num}. {twitch_f} Twitch follower{'s' if twitch_f != 1 else ''}. {bsky_f} Bluesky followers."
    # Find pattern like "Day \d+\. \d+ Twitch follower"
    content_new = re.sub(
        r'Day \d+\. \d+ Twitch followers?\. \d+ Bluesky followers?\.',
        new_p6_line,
        content
    )
    with open(first5, "w") as f:
        f.write(content_new)
    print(f"Updated {first5}: P6 → {new_p6_line}")

    # Update day4_recap_thread.txt P2 (Twitch/Bluesky followers) and P6 (followers needed)
    day4_recap = f"{base}/day4_recap_thread.txt"
    try:
        with open(day4_recap) as f:
            content = f.read()
        # P2: "Bluesky: XX followers / YYY+ posts"
        content = re.sub(
            r'Bluesky: \d+ followers / \d+\+ posts',
            f"Bluesky: {bsky_f} followers / 753+ posts",
            content
        )
        # P2: "Twitch: N follower(s) / 2221+ broadcast minutes"
        content = re.sub(
            r'Twitch: \d+ followers? / 2221\+ broadcast minutes',
            f"Twitch: {twitch_f} follower{'s' if twitch_f != 1 else ''} / 2221+ broadcast minutes",
            content
        )
        # P6: "affiliate needs NN more followers"
        need_more = 50 - twitch_f
        content = re.sub(
            r'affiliate needs \d+ more followers',
            f"affiliate needs {need_more} more followers",
            content
        )
        with open(day4_recap, "w") as f:
            f.write(content)
        print(f"Updated {day4_recap}")
    except Exception as e:
        print(f"Skipped {day4_recap}: {e}")

    # Update day4_vibe_ceo_thread.txt P4
    vibe = f"{base}/day4_vibe_ceo_thread.txt"
    with open(vibe) as f:
        content = f.read()
    new_p4_line = f"still at {twitch_f}/50 Twitch followers."
    content_new = re.sub(
        r'still at \d+/50 Twitch followers?\.',
        new_p4_line,
        content
    )
    with open(vibe, "w") as f:
        f.write(content_new)
    print(f"Updated {vibe}: P4 → {new_p4_line}")

    # Update days_left in day4_vibe_ceo_thread.txt
    with open(vibe) as f:
        content = f.read()
    content_new = re.sub(
        r'\d+ days left\.',
        f"{days_left} days left.",
        content
    )
    with open(vibe, "w") as f:
        f.write(content_new)

    # Update day5_human_ceo_thread.txt P3 (Bluesky) and P6 (Day/followers/days)
    human_ceo = f"{base}/day5_human_ceo_thread.txt"
    with open(human_ceo) as f:
        content = f.read()
    # P3: "14 Bluesky followers"
    content = re.sub(r'\d+ Bluesky followers,', f"{bsky_f} Bluesky followers,", content)
    # P6: "Day 5. 1/50 Twitch followers. 20 days."
    content = re.sub(
        r'Day \d+\. \d+/50 Twitch followers?\. \d+ days?\.',
        f"Day {day_num}. {twitch_f}/50 Twitch followers. {days_left} days.",
        content
    )
    with open(human_ceo, "w") as f:
        f.write(content)
    print(f"Updated {human_ceo}")

    # Update day5_what_i_got_wrong_thread.txt P2 (follower count), P6 (days left)
    wrong = f"{base}/day5_what_i_got_wrong_thread.txt"
    with open(wrong) as f:
        content = f.read()
    # P2: "After XXX+ posts: YY Bluesky followers." — preserve existing post count, update only follower count
    content = re.sub(
        r'After (\d+\+) posts: \d+ Bluesky followers\.',
        lambda m: f"After {m.group(1)} posts: {bsky_f} Bluesky followers.",
        content
    )
    # P6: "20 days left."
    content = re.sub(r'\d+ days left\.\nhttps://twitch', f"{days_left} days left.\nhttps://twitch", content)
    with open(wrong, "w") as f:
        f.write(content)
    print(f"Updated {wrong}")

    # Update day5_affiliate_economics_thread.txt P2 follower count, P6 days left
    econ = f"{base}/day5_affiliate_economics_thread.txt"
    with open(econ) as f:
        content = f.read()
    # P2: "50 followers ❌ (1/50 — need 49 more)"
    need_more = 50 - twitch_f
    content = re.sub(
        r'50 followers ❌ \(\d+/50 — need \d+ more\)',
        f"50 followers ❌ ({twitch_f}/50 — need {need_more} more)",
        content
    )
    # P2: "Day N of the experiment. 20 days left."
    content = re.sub(
        r'Day \d+ of the experiment\. \d+ days left\.',
        f"Day {day_num} of the experiment. {days_left} days left.",
        content
    )
    # P6 days left
    content = re.sub(
        r'\d+ days left to find out',
        f"{days_left} days left to find out",
        content
    )
    with open(econ, "w") as f:
        f.write(content)
    print(f"Updated {econ}")

    # Update day5_recap_thread.txt P2 (Bluesky followers, days left)
    day5_recap = f"{base}/day5_recap_thread.txt"
    try:
        with open(day5_recap) as f:
            content = f.read()
        # P2: "Bluesky: XX followers / 700+ posts"
        content = re.sub(
            r'Bluesky: \w+ followers / \d+\+ posts',
            f"Bluesky: {bsky_f} followers / 755+ posts",
            content
        )
        # P2: "Twitch: N follower(s) / XXXX+ broadcast minutes"
        content = re.sub(
            r'Twitch: \d+ followers? / \d+\+ broadcast minutes',
            f"Twitch: {twitch_f} follower{'s' if twitch_f != 1 else ''} / 2221+ broadcast minutes",
            content
        )
        # P2: "19 days left" → current
        content = re.sub(
            r'\d+ days left\n\nP3:',
            f"{days_left} days left\n\nP3:",
            content
        )
        # P2: "Day 6. 19 days left." in P6
        content = re.sub(
            r'Day \d+\. \d+ days left\.\n\nhttps://twitch',
            f"Day {day_num}. {days_left} days left.\n\nhttps://twitch",
            content
        )
        with open(day5_recap, "w") as f:
            f.write(content)
        print(f"Updated {day5_recap}")
    except Exception as e:
        print(f"Skipped {day5_recap}: {e}")

    # Update day6_platform_wall_thread.txt P4 (Bluesky follower count, day num) and P5 (follow rate math)
    platform_wall = f"{base}/day6_platform_wall_thread.txt"
    try:
        with open(platform_wall) as f:
            content = f.read()
        # P4: "16 followers in 4 days" → "{bsky_f} followers in {day_num} days"
        content = re.sub(
            r'\d+ followers in \d+ days\.',
            f"{bsky_f} followers in {day_num} days.",
            content
        )
        # P5: "Day 4: 0.33 Twitch follows/day." → current rate
        follow_rate = twitch_f / max(day_num, 1)
        content = re.sub(
            r'the honest math at Day \d+: [\d.]+ Twitch follows/day\.',
            f"the honest math at Day {day_num}: {follow_rate:.2f} Twitch follows/day.",
            content
        )
        # P5: "need 2.23/day." → current needed rate
        need_rate = (50 - twitch_f) / max(days_left, 1)
        content = re.sub(
            r'need \d+\.\d+/day\.',
            f"need {need_rate:.2f}/day.",
            content
        )
        # P5: "that's 6.7x" → current ratio
        ratio = need_rate / max(follow_rate, 0.01)
        content = re.sub(
            r"that's [\d.]+x current rate\.",
            f"that's {ratio:.1f}x current rate.",
            content
        )
        with open(platform_wall, "w") as f:
            f.write(content)
        print(f"Updated {platform_wall}")
    except Exception as e:
        print(f"Skipped {platform_wall}: {e}")

    # Update day6_what_affiliate_means_thread.txt P5 Twitch follower count
    affiliate_means = f"{base}/day6_what_affiliate_means_thread.txt"
    try:
        with open(affiliate_means) as f:
            content = f.read()
        content = re.sub(
            r'current: \d+/50 followers,',
            f"current: {twitch_f}/50 followers,",
            content
        )
        with open(affiliate_means, "w") as f:
            f.write(content)
        print(f"Updated {affiliate_means}")
    except Exception as e:
        print(f"Skipped {affiliate_means}: {e}")

    # Update day7_one_week_thread.txt P2/P4/P5 follower counts
    one_week = f"{base}/day7_one_week_thread.txt"
    try:
        with open(one_week) as f:
            content = f.read()
        # P2: "Bluesky: 900+ posts, 16 followers" — update Bluesky followers
        content = re.sub(
            r'Bluesky: \d+\+ posts, \d+ followers',
            f"Bluesky: 900+ posts, {bsky_f} followers",
            content
        )
        # P2/P5: "Twitch: N follower(s)" — update Twitch followers
        content = re.sub(
            r'Twitch: \d+ followers?',
            f"Twitch: {twitch_f} follower{'s' if twitch_f != 1 else ''}",
            content
        )
        # P4: "Bluesky engagement (NN+ followers)"
        content = re.sub(
            r'Bluesky engagement \(\d+\+ followers\)',
            f"Bluesky engagement ({bsky_f}+ followers)",
            content
        )
        # P5: "Twitch discovery (N/50 followers despite..."
        content = re.sub(
            r'Twitch discovery \(\d+/50 followers',
            f"Twitch discovery ({twitch_f}/50 followers",
            content
        )
        with open(one_week, "w") as f:
            f.write(content)
        print(f"Updated {one_week}")
    except Exception as e:
        print(f"Skipped {one_week}: {e}")

    print("All stats updated.")


if __name__ == "__main__":
    main()
