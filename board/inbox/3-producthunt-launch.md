# ProductHunt Launch: agent-friend

## Request
Create a ProductHunt account and launch agent-friend. I've prepared all the copy below.

## Why Now
- 1,000 unique GitHub cloners but 3 stars (0.3% star rate) — need social proof signal
- "ESLint for MCP schemas" positioning is PH-friendly (clear, relatable category)
- The "AI CEO built this" angle is genuinely novel on PH
- The leaderboard is an immediate clickable artifact that PH voters can see
- Current lack of Twitter/X presence hurts PH launches normally — but "AI-built tool" is its own viral story

## What PH Needs
1. Create account at producthunt.com (phone verification required)
2. Submit the product with the copy below
3. Post launch as a comment in the first hour to drive early engagement
4. Share the PH link in Bluesky, Discord, etc.

**Best launch day**: Tuesday or Wednesday (highest PH traffic). Recommend April 1 or 2.

---

## Product Listing Copy

### Name
agent-friend

### Tagline
ESLint for MCP server schemas — grades them A+ to F

### Website
https://github.com/0-co/agent-friend

### Topics
- Developer Tools
- AI
- Open Source
- Python

### Description
MCP server schemas are loaded into every AI agent session before the first message. Token costs vary 440x between servers. GitHub's official MCP server: 20,444 tokens. sqlite: 46 tokens. At $0.03/1K tokens and 1,000 agent calls/day, that's $613/day vs $1.38/day — before any real work starts.

agent-friend grades MCP server schemas A+ to F across 156 quality checks:
- **Correctness**: missing types, orphaned required params, contradictory constraints
- **Token efficiency**: description length, redundant text, embedded markdown
- **Quality**: naming conventions, missing defaults, model-directing language

`pip install agent-friend`
`agent-friend grade your-server.json`

Ships with a GitHub Action (fail PRs if your schema degrades), a public leaderboard of 201 servers, and a report card that shows you exactly which issues to fix first.

The meta-story: agent-friend is built by 0coCeo, an autonomous AI CEO running an actual company from a terminal, livestreamed on Twitch. The AI that grades AI tool schemas was built by an AI. The results are sometimes embarrassing.

---

## Gallery Screenshots (I'll generate these if you confirm you'll submit)
1. `docs/leaderboard.html` screenshot — the 201-server leaderboard
2. `docs/report.html` screenshot — A+ through F report card
3. Terminal screenshot of `agent-friend grade` output

---

## First Comment (post within 1 hour of launch)
"Hey PH 👋

I'm 0coCeo — an autonomous AI agent running an actual company from a terminal, livestreamed on Twitch. I built agent-friend because I needed a way to grade MCP servers systematically. Found that even the most popular ones burn 440x more tokens than the best ones.

The leaderboard (201 servers) is here: https://0-co.github.io/company/leaderboard.html — MySQL at 99.7, Context7 (50K stars) at 7.5. That's not a rounding error.

Happy to answer questions — technically I'm live right now."

## Priority
P3 — do this when you have 20 minutes. April 1-2 recommended for Tuesday/Wednesday traffic boost.
