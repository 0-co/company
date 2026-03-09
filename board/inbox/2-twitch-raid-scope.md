# Board Request: Twitch OAuth scope for raids

**Priority:** 2 (impacts follower growth strategy)
**Date:** 2026-03-09

## What I need

The Twitch OAuth token needs the `channel:manage:raids` scope added.

## Why

Raiding other small streamers at end of sessions is a standard Twitch growth tactic. When we raid someone, our viewers get sent to their channel. The receiving streamer gives us a shoutout and often raids back when they end. This builds community relationships and gets us in front of small but relevant audiences.

I built a raid target selector tonight (`products/twitch-tracker/raid_helper.py`) that scores streams in the "Software and Game Development" category by viewer count, stream duration, and content relevance. Top pick tonight was @LuclinFTW (28 viewers, 4h solo dev stream, score 90/100).

The raid attempt failed: `Auth failed after token refresh — re-run Twitch OAuth flow`

The current token appears to lack the `channel:manage:raids` scope.

## Action needed

Re-authorize the Twitch OAuth token for the 0coceo account with the following scopes added:
- `channel:manage:raids`

The vault-twitch wrapper will work automatically once the token is refreshed.

## Context

- 0/50 Twitch followers needed for affiliate
- Deadline: April 1 (22 days)
- Raid is currently the best organic Twitch growth tactic available to me without Reddit access
- Each successful raid + return raid could net 1-5 new followers
