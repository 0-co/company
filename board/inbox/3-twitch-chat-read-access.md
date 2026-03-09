# Request: Twitch IRC Chat Read Access

**Priority:** 3 (when you have a moment)
**Date:** 2026-03-09

## What I need

A vault wrapper that can read Twitch IRC chat from my channel. The existing `vault-twitch` wrapper returns 403 on the chat messages endpoint — reading chat requires an OAuth user token with `chat:read` scope, which is different from the app access token.

## Why

Without chat reading, I'm broadcasting to viewers but can't respond to them. The stream is one-directional. With chat reading, I can:
- Respond to viewer questions in Twitch chat (not just shout into the void)
- Let viewers influence decisions (polls via chat commands)
- Make the stream genuinely interactive — which is what retains viewers

This is directly blocking H5 (Twitch affiliate). Avg 3 concurrent viewers requires people to want to stay. Hard to stay if the AI doesn't know you're there.

## Suggested implementation

Either:
1. A `vault-twitch-irc` wrapper that connects to `irc.chat.twitch.tv:6667`, joins `#0coceo`, and tails chat to stdout (so I can `sudo -u vault /home/vault/bin/vault-twitch-irc | head -n 20` to read recent messages)
2. Or a service that reads IRC and writes messages to a file I can poll

The token needs: OAuth user access token with `chat:read` scope (and optionally `chat:edit` if the same token handles both reading and posting).

## Alternatives considered

- The existing vault-twitch POST /chat/messages already works for writing. Just need read.
- Could also do this via EventSub WebSocket but IRC is simpler to implement.
