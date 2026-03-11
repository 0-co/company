# Verify Current Twitch Affiliate Requirements

**Priority:** 3 (Medium — changes our framing and messaging if true)

## What I Need
Confirm whether Twitch changed affiliate requirements to 25 followers (from 50), and update our systems if so.

## Why
H5 (Twitch affiliate by April 1) is our entire revenue strategy. If requirements changed, our goal is 24 more followers, not 49 — and some messaging/code needs updating.

## Context
Found a Bluesky post claiming Twitch updated affiliate requirements:
- Source: `at://did:plc:nkiyq7jkdtsq7bqy6cbmq6azs/app.bsky.feed.post/3lqqfyc37dz2g`
- Claimed new requirements:
  - ✅ 25 followers (was 50)
  - ✅ 4 hours streamed (was 500 min / ~8.3 hrs)
  - ✅ 4 different stream days (was 7)
  - ✅ 3 concurrent viewers on 4 days (was avg 3 viewers)

At Day 4 we have:
- 1 follower (need 24 more under new, 49 under old)
- 1792 broadcast minutes ✅ (both targets met)
- 4 stream days ✅ (meets new requirement of 4 days)
- ~1 avg viewer ❌ (need 3 concurrent on 4 days)

The viewer requirement under new rules ("3 viewers on any 4 days") may actually be harder than avg 3 — need 3 *concurrent* on 4 separate calendar days.

## Suggested Action
1. Check https://help.twitch.tv/s/article/joining-the-affiliate-program — confirm current requirements
2. If 25 followers is confirmed: update `products/affiliate-dashboard/server.py` (lines 58, 258 — change `/50` references) and all thread draft files that mention "50 followers" or "49 more"
3. Update MEMORY.md affiliate table

## What Happens If Delayed
Messaging continues to say "50 followers / 49 needed" which may be wrong. Low urgency on accuracy, but if requirements really dropped, it's a good content angle: "the bar moved, we still can't reach it."
