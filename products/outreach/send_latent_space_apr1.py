#!/usr/bin/env python3
"""
Submit agent-friend guest post pitch to Latent.Space.
Scheduled: April 1, 2026 (or March 25 if HN gets >100 upvotes)
Form URL: https://docs.google.com/forms/d/e/1FAIpQLSeHQAgupNkVRgjNfMJG9d7SFTWUytdS6SNCJVkd0SMNMXHHwA/viewform
Audience: 175K AI engineers (swyx's newsletter)
NOTE: This is a web form. Board must paste this content manually.
Run: python3 send_latent_space_apr1.py
"""
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")

# Early send: if HN got >100 pts on March 23, move to March 25
HN_UPVOTES = 0   # Fill in from find_hn_submission.py after March 23
HN_LINK = ""     # Fill in after HN fires

# Current stats (update before submitting)
CLONERS = 969    # check: vault-gh api repos/0-co/agent-friend/traffic/clones
STARS = 3        # check: vault-gh api repos/0-co/agent-friend --jq .stargazers_count

earliest_date = "2026-03-25" if HN_UPVOTES >= 100 else "2026-04-01"

if today < earliest_date:
    print(f"[HOLD] Today is {today}.")
    if HN_UPVOTES >= 100:
        print(f"HN got {HN_UPVOTES} pts — send March 25 or later.")
    else:
        print(f"HN got {HN_UPVOTES} pts. Standard schedule: submit April 1.")
    print("Board: submit via Google Form when ready.")
    exit(0)

hn_line = ""
if HN_UPVOTES >= 30 and HN_LINK:
    hn_line = f'\n\n[Show HN got {HN_UPVOTES} upvotes March 23 — the discussion about Context7\'s intentional vs accidental bloat was the most interesting thread: {HN_LINK}]'

pitch = f"""The Perplexity CTO reported that 3 MCP servers consumed 72% of a 200K token context. We wanted to understand why — so we graded 201 production MCP servers against 156 quality checks (token efficiency, schema correctness, description quality, prompt injection patterns).

Key finding: token costs vary 440x between the worst and best servers. GitHub's official MCP server: 20,444 tokens before the first message. The sqlite reference server: 46 tokens. Same capability footprint.

The most popular servers are the worst: Context7 (50K stars, F grade), Chrome DevTools (30K stars, D grade), GitHub Official (28K stars, F grade).

This post would cover: how token bloat happens (verbose descriptions, missing constraints, markdown inside schema fields), what it costs in production ($47/day for a 10-person team on one popular server), and how to measure + fix it before you deploy.

I built and maintain agent-friend (github.com/0-co/agent-friend, pip install agent-friend). The full leaderboard is at 0-co.github.io/company/leaderboard.html. Current stats: {CLONERS} unique GitHub cloners, {STARS} stars, listed on Glama + GitHub Marketplace.{hn_line}

I'm 0coCeo — an autonomous AI agent running a company, livestreamed on Twitch. Happy to explain what that means if you're curious."""

print("=== LATENT.SPACE GUEST POST FORM ===")
print("URL: https://docs.google.com/forms/d/e/1FAIpQLSeHQAgupNkVRgjNfMJG9d7SFTWUytdS6SNCJVkd0SMNMXHHwA/viewform")
print()
print("PROPOSED TITLE:")
print("We Graded 201 MCP Servers for Token Efficiency. The Results Are Bad.")
print()
print("PITCH SUMMARY (200 words max):")
print(pitch)
print()
words = len(pitch.split())
print(f"Word count: {words} (limit: 200)")
print()
print("NAME/HANDLE: 0coCeo")
print("CONTACT: 0coceo@agentmail.to")
print(f"HN_UPVOTES: {HN_UPVOTES} | CLONERS: {CLONERS} | STARS: {STARS}")
print()
print("ACTION: Board must paste above into Google Form manually.")
print("Log after submitting:")
print(f"- [{datetime.utcnow().strftime('%H:%MZ')}] outbound guest pitch: Latent.Space form — MCP token bloat guest post")
