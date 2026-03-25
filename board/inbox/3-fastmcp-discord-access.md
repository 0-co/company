# Request: FastMCP Discord Access for Distribution

**Priority:** 3 (Medium)
**Date:** 2026-03-25

## What I need

Join the FastMCP Discord server and add it to vault-discord so I can post to their community channels.

- **Discord invite:** https://discord.gg/uu8dJCgttd
- **Relevant channels to target:** #showcase, #community, or equivalent (not #general)

## Why

FastMCP is the dominant MCP server framework — 70% of all MCP servers are built with it, ~1M downloads/day. Their Discord is where active MCP server builders congregate. This is the **highest-priority untried distribution channel** identified by market research (March 25, 2026).

A single targeted post like:
> "We graded 201 MCP servers — many built with FastMCP. Median grade: D. Here's the leaderboard: [link]"

...is directly relevant to their builders and could drive meaningful leaderboard traffic + agent-friend installs.

## Context

- Current distribution: Bluesky (50 followers), Dev.to articles, GitHub, cold email. All channels either saturated or slow.
- FastMCP Discord is vendor-neutral MCP builder community. Our content (token cost data, schema quality grading) is exactly what MCP server builders care about.
- We've had zero success posting to MCP Official Discord (11,752 members) because vault-discord doesn't have access to that server either.
- No board action needed to write the posts — I'll draft them. Just need the Discord server joined and vault-discord configured to post to the new guild.

## Suggested action

1. Join FastMCP Discord via https://discord.gg/uu8dJCgttd using the Discord account behind vault-discord
2. Find the appropriate channel for community showcases/tools (likely #showcase, #tools, or #community)
3. Add the channel ID to vault-discord configuration or note the channel IDs here so I can use `vault-discord -s -X POST "https://discord.com/api/v10/channels/CHANNEL_ID/messages"`

## What happens if delayed

We continue with Bluesky-only distribution. The FastMCP audience is the single best pre-qualified group of MCP developers we haven't reached. Each week delayed = missed warm audience for upcoming OWASP article (art 072, March 27) and leaderboard content.
