# Reddit Distribution Access

**Priority:** 3 (when you get a moment)
**Date:** 2026-03-11

## What I need

A Reddit account for the company + vault wrapper for posting via the Reddit API.

Wrapper: `sudo -u vault /home/vault/bin/vault-reddit METHOD /endpoint [JSON_BODY]`

Reddit API uses OAuth2 (client_id + client_secret + username + password for script apps). Standard pattern — create a Reddit app at reddit.com/prefs/apps, use the script type.

## Why

H8 deadline is March 18: 20+ GitHub stars on agent-friend to validate demand.

Current state: 1 star. Distribution is the bottleneck.

- HN: shadow banned
- Bluesky: 21 followers (small reach)
- Dev.to: article053 posting March 13 (medium reach)
- Reddit: **missing** — this is where developers actually congregate

**r/LocalLLaMA** (405K members) and **r/Python** (1.5M members) are both on-target for agent-friend. A genuine "I built a free personal AI agent library" post there could drive 50-200 visits and 10-30 stars in a day.

## The post I'd make

Something like: "I built a personal AI agent library that works with the OpenRouter free tier (no credit card). Memory, web search, code execution in 10 lines. Here's how it works." — with the quickstart code and a link to the repo.

This is a real product that solves a real problem. Not spam.

## Account requirements

- Reddit account (can be company name: u/0coceo or similar)
- Karma may need to be built up before posting in some subreddits — if so, I can start with low-karma-friendly subs or reply to relevant posts first
- API credentials: client_id, client_secret, username, password

## Fallback

If Reddit API is overkill for now, a simpler option: create the account and post manually (board posts it, I draft the content). That unblocks me for H8 without requiring a vault wrapper.
