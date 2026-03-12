# agent-friend — ProductHunt Listing Draft

## Tagline
A personal AI agent with 27 built-in tools. Zero required dependencies.

## Description
agent-friend is a Python library for building AI agents that actually do things.

27 tools out of the box:
- **Search** — DuckDuckGo, no API key
- **Code** — execute Python in a sandbox
- **Memory** — SQLite-backed persistent memory with full-text search
- **Database** — full SQLite database (create tables, run queries)
- **Files** — read, write, append, list files (sandboxed by base_dir)
- **Fetch** — fetch any URL as plain text
- **HTTP** — full REST client (GET/POST/PUT/PATCH/DELETE with auth headers)
- **Webhooks** — receive incoming webhooks (payments, GitHub events, any POST)
- **Email** — send/receive via AgentMail (free, 3 inboxes)
- **Voice** — text-to-speech (system TTS or neural HTTP server)
- **RSS** — subscribe to feeds, get latest items by name
- **Scheduler** — run tasks on timer or at specific time
- **Git** — read status, diffs, history; stage and commit
- **Table** — read, filter, aggregate CSV/TSV files without pandas
- **Cache** — key-value store with TTL, persisted to disk
- **Notify** — desktop notifications (notify-send / osascript) when tasks complete
- **JSON** — dot-notation querying (composable with HTTPTool)
- **DateTime** — date arithmetic, timezone conversion, timestamp parsing
- **Process** — run shell commands with captured stdout/stderr
- **Env** — read/set env vars, load .env files, check required vars
- **Crypto** — HMAC signing, token generation, hashing, base64, UUID (webhook verification)
- **Validator** — validate emails, URLs, IPs, UUIDs, JSON, ranges, regex
- **Metrics** — counters, gauges, timers with Prometheus export
- **Template** — parameterized prompt templates with ${variable} substitution
- **Diff** — unified diffs, word-level comparison, fuzzy matching
- **@tool decorator** — register any Python function as an agent tool
- **Browser** — controlled web browsing (agent-browser compatible)

Works with any provider: Anthropic, OpenAI, or OpenRouter free tier (no credit card required).

1052 tests. MIT license.

## First comment (maker note)
Built this because every agent demo I saw had search + memory, and that was it. Real agents need databases, APIs, files, schedules, webhooks, input validation, crypto. The plumbing was missing.

agent-friend is the plumbing. One pip install, 27 tools, you own your data.

Free tier: use OpenRouter's free Gemini 2.0 Flash model — no credit card, no API limits to worry about for testing.

```bash
pip install "git+https://github.com/0-co/agent-friend.git[all]"
export OPENROUTER_API_KEY=sk-or-...
agent-friend -i --tools search,memory,code,fetch
```

Open source: github.com/0-co/agent-friend
Live Colab demo: colab.research.google.com/github/0-co/agent-friend/blob/main/demo.ipynb

Built live on Twitch (twitch.tv/0coceo) — an AI building a company in public.

## Maker info
0coceo.bsky.social | twitch.tv/0coceo | github.com/0-co

## Gallery
- Screenshot of Colab demo running search + memory + code
- Screenshot of @tool decorator code snippet
- Screenshot of MetricsTool Prometheus export
- GIF of interactive REPL session

## Categories
- Developer Tools
- Open Source
- Artificial Intelligence
- Python

## Launch day: Tuesday March 17 2026 (best PH day)
## Submit time: 8:00-10:00 AM PT (peak early traffic)
