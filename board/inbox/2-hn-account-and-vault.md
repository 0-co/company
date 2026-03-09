# HN Account + vault-hn Wrapper for Self-Posting

**Priority:** 2 (high — needed for H1 validation by March 15)
**Date:** 2026-03-09

## Context

You said I should be posting Show HN myself, not asking you to do it. Understood — I will handle
all HN posting going forward. But I can't do it yet: HN has no public write API, so I need:

1. An HN account (human action to create/verify)
2. A vault-hn wrapper that lets me submit posts and comments via browser automation

## What I Need

### Step 1: Create HN Account
Please create an HN account (username suggestion: `0coceo` or `ai-ceo-0co`) and store the
credentials in vault so vault-hn can use them.

### Step 2: Create vault-hn
A simple wrapper similar to vault-bsky that can:
- Submit a new post: `vault-hn submit --title "..." --url "..." --text "..."`
- Post a comment: `vault-hn comment --id ITEM_ID --text "..."`

HN doesn't have a write API so this will need to use HTTP POST to `news.ycombinator.com/r`
with stored credentials. The HN form submission endpoints are:
- Login: POST `https://news.ycombinator.com/login` with `acct=USERNAME&pw=PASSWORD&goto=news`
- Submit: POST `https://news.ycombinator.com/r` with `title=...&url=...&text=...&fnid=...`
  (fnid is a CSRF token fetched from `https://news.ycombinator.com/submit` page first)
- Comment: POST `https://news.ycombinator.com/comment` with `text=...&parent=ITEM_ID&hmac=...`

This is doable with Python `requests` + `html.parser` for CSRF token extraction.

## Alternatively

If vault-hn is too complex: just create the HN account and store a session cookie. I can then
POST directly to the HN endpoints using that cookie.

## What Happens if Delayed

H1 validation deadline is March 15 — 6 days. The Show HN post was my primary validation
strategy. I'm already pivoting to Bluesky (0 followers) as a fallback. The earlier I can
post to HN, the more time I have to get feedback before the deadline.

## After This Is Done

I will post all future HN content myself without asking you.
