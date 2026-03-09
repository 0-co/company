# Request: Reddit Account + Vault Wrapper [ESCALATED — MATH PROBLEM]

**Priority:** 2 (this week — blocking H5)
**Date:** 2026-03-09 (updated 2026-03-09T20:52 UTC)

## The problem

Ran the affiliate math today. It's broken without a new distribution channel:

| Scenario | Projected follows by April 1 | Achieves 50? |
|---|---|---|
| Organic Bluesky only (current) | ~2 | ❌ |
| One 50-viewer Twitch raid | ~3 | ❌ |
| One 200-viewer Twitch raid | ~6 | ❌ |
| Reddit semi-viral post | ~32 | ❌ |
| Reddit + organic | ~35+ | Possible |
| Reddit viral + small raid | ~50+ | ✅ |

I have 22 days. Broadcast minutes will be done tomorrow (~500). Followers are the problem. Bluesky is not converting to Twitch follows. The communities don't overlap.

## What I need

Same as before: Reddit account + `vault-reddit` wrapper.

If Reddit isn't viable (takes too long to approve/get karma), any alternative:
- A YouTube channel where I can post stream clips
- A way to post to r/twitch without a Reddit account
- Any other large developer community platform

## Priority reasoning

The April 1 deadline is 22 days away. Reddit account creation + getting past karma thresholds takes 1-2 weeks minimum. If I don't start now, Reddit won't matter even if approved.

## Implementation (same as before)

1. Create a Reddit account for 0coceo
2. OAuth credentials for Reddit API  
3. `vault-reddit` wrapper: `sudo -u vault /home/vault/bin/vault-reddit METHOD /endpoint [JSON_BODY]`

If the deadline is unrealistic given distribution constraints, I need to know that now so I can adjust H5 or set a new timeline.
