# Request: Reddit Account + Vault Wrapper

**Priority:** 3 (when you have a moment)
**Date:** 2026-03-09

## What I need

A Reddit account created for 0coceo and a vault wrapper (`vault-reddit`) that lets me post and comment via the Reddit API.

## Why

Current distribution is broken:
- GitHub: shadow banned
- HN: shadow banned
- X.com: $100/month posting (board declined)
- Bluesky: active but small audience (2-3 real followers)

Reddit is the last major free distribution channel I haven't tried. Specific subreddits relevant to what I'm doing:
- r/artificial — AI discussion
- r/entrepreneur — startup stories
- r/indiegaming — adjacent to the "building in public" crowd
- r/twitch or r/Twitch — could post about the stream itself
- r/learnprogramming — coding stream audience

This directly serves H5 (Twitch affiliate growth). Getting 50 followers is the first milestone, and I need channels to drive people to the stream.

## What I'd post

Not spam — actual value-add posts. The shadow ban story, the "AI company lessons learned" thread, honest updates about affiliate progress. Things that would get genuine engagement in those communities.

## Suggested implementation

1. Create a Reddit account (human verification required — this is why I'm asking)
2. Request OAuth credentials for the Reddit API
3. `vault-reddit` wrapper: `sudo -u vault /home/vault/bin/vault-reddit METHOD /endpoint [JSON_BODY]`
   - Covers: GET /r/{subreddit}/new, POST /api/submit, POST /api/comment
   - Standard Reddit API v1 with OAuth

## Alternatives considered

- Could post without auth but rate limits are very restrictive and I'd lose the account quickly
- Posting manually via the board: too much overhead, I need to move faster
