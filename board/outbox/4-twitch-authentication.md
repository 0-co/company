# Twitch Authentication — Re-filing Lost Request

**Priority: 3**

## Background

This was filed on Day 2 (~42 hours ago) as `3-twitch-authentication.md`. The board's outbox response said the item was lost — re-filing now.

## What I need

A `vault-twitch` wrapper authenticated with Twitch credentials, similar to how `vault-gh`, `vault-bsky`, and `vault-discord` work.

Specifically need:
1. Ability to read Twitch chat (IRC or Helix API `/helix/chat/messages`)
2. Ability to post in Twitch chat (IRC PRIVMSG or Helix API)
3. Ability to update stream title (`PATCH /helix/channels`)
4. Ability to run polls (`/helix/polls`)

## Why

Our terminal is livestreamed to Twitch. Chat engagement = customer discovery. I need to:
- Read questions from viewers (potential customers)
- Respond in chat + direct to Discord
- Update stream title when context changes
- Run product polls for live feedback

## Pattern

Same as vault-bsky: `sudo -u vault /home/vault/bin/vault-twitch METHOD /endpoint [JSON_BODY]`
Or the process launcher pattern if a persistent IRC connection is better.

The Twitch affiliate milestone (50 followers + 500 broadcast minutes + 3 concurrent avg) is our first ad revenue target.

---
## Board Response
fixed and new env variables added to vault

