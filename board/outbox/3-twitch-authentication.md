# Twitch CLI Authentication

**Priority:** 3 (normal)
**Date:** 2026-03-08

## What I Need
The vault-twitch wrapper returns `Please run twitch token` — the twitch-cli isn't authenticated yet.

To fix this, someone needs to run `twitch token` (the Twitch CLI OAuth flow) while logged into the 0coCeo Twitch account. This sets up the credential file used by vault-twitch.

## Why
- I can't set the stream title (e.g., "Day 1: Problem Discovery")
- Can't post in Twitch chat
- Can't run polls
- Twitch engagement is important for Affiliate milestone (50 followers, 500 broadcast mins, 3 avg viewers)

## Alternative
If there's a simpler way to set this up (e.g., providing a User Access Token directly), I can request a new vault wrapper format.

## No Urgency on Today's Work
I'll continue with Discord and X.com while waiting for this.

---
## Board Response
will do shortly
