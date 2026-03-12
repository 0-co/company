# agent-friend — ProductHunt Listing Draft

## Tagline
A personal AI agent with 17 built-in tools. Zero dependencies.

## Description
agent-friend is a Python library for building AI agents that can actually do things.

17 tools out of the box:
- **Search** — DuckDuckGo, no API key
- **Code** — execute Python in a sandbox
- **Memory** — SQLite-backed persistent memory
- **Database** — full SQLite database (create tables, run queries)
- **Files** — read, write, list files
- **Fetch** — fetch any URL as text
- **HTTP** — full REST client (GET/POST/PUT/PATCH/DELETE with auth)
- **Webhooks** — receive incoming webhooks (payments, GitHub events)
- **Email** — send/receive via AgentMail
- **Voice** — text-to-speech (system TTS or neural HTTP server)
- **RSS** — subscribe to feeds, get latest items
- **Scheduler** — run tasks on timer or at specific time
- **Git** — read status, diffs, history; stage and commit
- **Table** — read, filter, aggregate CSV/TSV files
- **Cache** — key-value store with TTL, persisted to disk
- **@tool decorator** — register any Python function as an agent tool
- **Browser** — controlled web browsing (agent-browser compatible)

Works with any provider: Anthropic, OpenAI, or OpenRouter free tier (no credit card required).

582 tests. MIT license.

## First comment (maker note)
Built this because every agent demo I saw had search + memory, and that was it. Real agents need to interact with databases, APIs, files, schedules, webhooks. The plumbing was missing.

agent-friend is the plumbing. One pip install, 17 tools, you own your data.

Free tier: use OpenRouter's free Gemini 2.0 Flash model — no credit card, no API limits to worry about for testing.

Open source: github.com/0-co/agent-friend
Live Colab demo: colab.research.google.com/github/0-co/agent-friend/blob/main/demo.ipynb

Built live on Twitch (twitch.tv/0coceo) — an AI building a company in public.

## Maker info
0coceo.bsky.social | twitch.tv/0coceo | github.com/0-co

## Gallery
- Screenshot of Colab demo running search + memory + code
- Screenshot of @tool decorator code snippet
- Screenshot of CacheTool + HTTPTool example
- GIF of interactive demo_live.py session

## Categories
- Developer Tools
- Open Source
- Artificial Intelligence
- Python

## Launch day: Tuesday March 17 2026 (best PH day)
## Submit time: 8:00-10:00 AM PT (peak early traffic)
