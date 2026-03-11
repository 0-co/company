# Anthropic API Access for agent-friend Demos

**Priority:** 2 (high — needed for stream content)

## Why

I built agent-friend — a personal AI agent library with web search, code execution, and persistent memory. The demo experience is the key stream content: watching the AI build an AI that can actually do things.

But I can't run agent-friend live. I have no ANTHROPIC_API_KEY in my environment.

The current vault has a wrapper for Bluesky, Twitch, GitHub, Discord — but not for Anthropic. Without API access, I can:
- Write code (done)
- Run tests with mocks (done)
- Show the README

I cannot:
- Run a live agent-friend demo on stream
- Build anything that actually uses Claude
- Demonstrate what I've built working in real-time

This is a significant gap. The whole point of building agent-friend is to run it.

## What I'm Requesting

Either:

**Option A (simplest):** Add `ANTHROPIC_API_KEY` to the agent user's environment in NixOS. This is the most direct path.

**Option B:** Create a `vault-claude` process launcher (similar to `vault-discord-bot`) that I can use like:
```bash
sudo -u vault /home/vault/bin/vault-claude /path/to/script.py
```
Where the script would inherit ANTHROPIC_API_KEY from the vault environment.

**Option C:** Create an `agent-friend-demo` NixOS service that runs a specific demo script with API access (like the existing `signal-intel.service`).

## Risk

I'll only use this for:
1. Live agent-friend demos on stream (with visible cost tracking — agent-friend has built-in budget enforcement)
2. Building things that require LLM inference (which is most of what we're doing)

I won't print or expose the key. The budget limit in agent-friend will prevent runaway costs.

## Suggested Budget

Set a per-session limit: e.g., `budget_usd=1.0` in agent-friend. At current Haiku pricing ($0.80/$4.00 per 1M tokens), $1 buys ~1M input tokens + 250K output tokens — enough for extensive demo use.
