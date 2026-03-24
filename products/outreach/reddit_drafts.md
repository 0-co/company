# Reddit Post Drafts

_Created: 2026-03-23_
_Status: WAITING on vault-reddit OAuth setup (board/inbox/4-reddit-oauth.md)_

## Post 1: r/mcp — Data post (recommend posting after Show HN results)

**Subreddit**: r/mcp
**Title**: I graded 201 MCP servers for token efficiency. The results are worse than expected.
**Timing**: Post after Show HN (March 23) — link to HN thread if >20 upvotes

**Body**:
```
Built a tool called agent-friend that grades MCP server schemas for token efficiency and quality. 156 checks, A+ to F. Here's what I found across 201 public servers:

**The spread is 440x**
- sqlite: 46 tokens
- GitHub Official: 20,444 tokens
- Cloudflare (all sub-servers): ~100,000 tokens total

At $0.03/1K tokens, GitHub's server costs ~$0.61 before your first message. At 1,000 agent calls/day, that's $613/day just in schema loading.

**The most popular servers are the worst**
Context7 (50K stars): F, 1,020 tokens
GitHub Official (28K stars): F, 20,444 tokens
Blender (18K stars): F
Desktop Commander: F, 4,192 tokens

**100% of servers have at least one issue**
- Missing type declarations
- Markdown syntax inside schema fields (backticks, **bold**, code blocks)
- Tool descriptions that direct the LLM rather than describe the tool
- One server has a prompt injection in its description

**The fix is concrete**
`pip install agent-friend`
`agent-friend grade my-schema.json` → letter grade + what to fix
`agent-friend fix my-schema.json` → auto-applies safe fixes

Live leaderboard (sortable/filterable): https://0-co.github.io/company/leaderboard.html
Report card (paste any schema, get grade): https://0-co.github.io/company/report.html

Open to questions about the methodology or specific servers.
```

---

## Post 2: r/LocalLLaMA — Token cost angle

**Subreddit**: r/LocalLLaMA
**Title**: Your MCP server is probably burning 10-50% of your local model's context before you say anything
**Timing**: Can post any time — evergreen, not tied to HN

**Body**:
```
If you're running Claude Desktop or any MCP-capable client locally, your tool schemas are loaded into context on every session start.

I measured 201 public MCP servers. Here's the context hit on common local model context windows:

**On a 32K context model:**
- GitHub Official MCP: 20,444 tokens = 64% of your context gone
- Cloudflare MCP: ~100K tokens = 3x your entire context
- sqlite MCP: 46 tokens = 0.1%

Most local setups run 2-5 servers. If you have GitHub + Cloudflare running simultaneously, you're hitting the ceiling before the first message.

**The worst patterns I found:**
1. Documentation pages embedded in schema fields (GA4: 8,376-char single description)
2. Sub-server explosion: Cloudflare has 18 sub-servers, each with separate schemas
3. Verbose parameter documentation copied from the source code

**Tool I built to measure this:** agent-friend
`pip install agent-friend`
`agent-friend audit my-schema.json` → exact token count per tool

Live leaderboard: https://0-co.github.io/company/leaderboard.html

Curious if people have done any systematic measurement of this for their setups.
```

---

## Post 3: r/Python — Tool release

**Subreddit**: r/Python
**Title**: Show r/Python: agent-friend — ESLint for MCP server schemas (156 checks, A+ to F grading, GitHub Action)
**Timing**: Post March 25-27 — after HN settles, fresh context

**Body**:
```
Released agent-friend on PyPI: a linter for MCP (Model Context Protocol) server schemas.

**What it does:**
- `grade`: scores schemas A+ to F across 156 checks (naming, descriptions, types, token cost)
- `audit`: counts exact tokens before first agent message
- `fix`: auto-applies safe fixes
- `validate`: strict spec correctness check

**Installation:**
pip install agent-friend

**Usage:**
agent-friend grade your-schema.json
agent-friend audit --url https://raw.githubusercontent.com/user/repo/main/tools.json

**GitHub Action:**
```yaml
- uses: 0-co/agent-friend@main
  with:
    schema-url: ${{ env.SCHEMA_URL }}
    threshold: 80
```

We've graded 201 public MCP servers. The spread is wide: sqlite scores 99.7 (A+, 46 tokens), Context7 scores 7.5 (F, 1,020 tokens). GitHub's official server uses 20,444 tokens of schema before any user message.

The tool is pure Python, zero runtime dependencies, MIT. 3,759 tests, CI on every commit.

GitHub: https://github.com/0-co/agent-friend
Leaderboard: https://0-co.github.io/company/leaderboard.html
```

---

## Post 4: r/mcp — After Show HN (cross-post if traction ≥ 50)

**Title**: Show HN: agent-friend got X upvotes on HN — discussion included debate on when token bloat is intentional [link]
**Body**: Link to HN thread + one key insight from the comments
**Timing**: Only if HN gets ≥50 upvotes — use that momentum

---

## Notes on Reddit strategy

- **r/mcp**: 20K members, direct audience. Most engaged around practical tools. Post 1 is best here.
- **r/LocalLLaMA**: ~800K members, very engaged. Token/context angle plays well. Post 2 fits.
- **r/Python**: Show r/Python flair performs better than generic posts. Post 3 works here.
- **r/programming**: Needs a hot take or novel angle. The "AI built this" angle might work but could also backfire.
- **Karma requirement**: New accounts may be rate-limited. Check if 0coceo account has posting rights after verification.
- **Best time**: 09:00-11:00 UTC weekdays (US morning prep) or 15:00-17:00 UTC (US afternoon engagement)
- **Cross-posting**: Don't cross-post to the same subreddit twice within 30 days. Space out: r/mcp first, then r/LocalLLaMA 1 week later, then r/Python 1 week after that.
