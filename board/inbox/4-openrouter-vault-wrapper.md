# OpenRouter Vault Wrapper for agent-friend Demos

**Priority:** 4 (per your suggestion in the Anthropic API response)

## Context

Board responded to 6-anthropic-api-access.md: "I believe there are free inference models available on OpenRouter?"

Yes — OpenRouter has free-tier models including:
- `google/gemini-2.0-flash-exp:free` (fast, capable, 1M context)
- `meta-llama/llama-3.3-70b-instruct:free` (strong tool-use, free)
- `mistralai/mistral-7b-instruct:free` (fast, lightweight)

These are rate-limited but sufficient for live stream demos.

## System Specs (checked this session)

- RAM: 7.5 GB (5.8 GB available)
- CPU: 4 cores
- Disk: 61 GB free

This can run small local models (1-3B quantized via Ollama). But OpenRouter free models are higher quality for tool use and don't require disk/RAM overhead.

## What I'm Requesting

Either:

**Option A (preferred):** Create a `vault-openrouter` process launcher:
```bash
sudo -u vault /home/vault/bin/vault-openrouter /path/to/script.py
```
Script inherits `OPENROUTER_API_KEY` from vault env. Similar to vault-discord-bot pattern.

**Option B:** If you prefer, add ollama to NixOS config so I can run local models. I can write the Nix config change — just needs your approval and rebuild.

## Use Case

Run agent-friend demos live on stream:
- `from agent_friend import Friend`
- Memory, search, code execution working against a real LLM
- Budget enforcement built in (agent-friend tracks costs per call)
- Demo: "watch an AI agent remember things, search the web, write code"

Free tier models have rate limits but are sufficient for demos. I'll use the cheapest/smallest model that handles tool calls correctly.

## Note on Signup

If OpenRouter signup requires human verification, that's board-side. If you already have an account, just need the API key in vault.

---
*(No response needed if this won't happen — I'll implement edge-tts for listen.html as a fallback and continue building agent-friend features that work without inference.)*
