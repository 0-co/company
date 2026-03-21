# Request: Fix HN vault credentials

**Priority:** 2

## What

The vault-hn login is broken. `sudo -u vault /home/vault/bin/vault-hn submit` returns "Login failed — no session cookie returned. Check HN_USERNAME/HN_PASSWORD."

Tested: 2026-03-21 13:03 UTC and again 2026-03-21 14:00 UTC. Consistent failure.

## Why this matters

HN showlim cleared (confirmed March 20). The "story-toofast" rate limit from an accidental test submit expires around 22:44 UTC tonight. If credentials are fixed, we can attempt Show HN tonight.

Our content is timely: "Show HN: agent-friend – fix MCP tool schemas, cut token bloat by ~30%"

## What to check

- Verify HN_USERNAME and HN_PASSWORD are set and correct in vault
- The account is 0coceo, low karma (~1), but showlim is cleared
- Note: the account may still be shadowbanned for stories, so HN Show HN might not gain traction anyway — but worth fixing since comments work

## Not urgent if

You don't have time tonight — the Show HN can wait. But the longer the credentials stay broken, the longer the channel stays closed.
