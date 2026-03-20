# HN Submission Draft
# Use when showlim lifts. Verify score still accurate before submitting.
# Last updated: 2026-03-20

## Option A: Show HN — fix-first angle (PREFERRED, updated 2026-03-20)

**Title:** Show HN: agent-friend – cut your MCP server's token cost in one command

**URL:** https://github.com/0-co/agent-friend

**Comment to post immediately after:**

Built this after noticing that most AI agent failures weren't bugs — they were schema quality problems. Tools with vague descriptions, missing constraints, enums with no defaults. The model guesses wrong and the tool fails.

The tool has two modes:

1. `agent-friend grade server.json` — scores 0-100 across 149 checks (token waste, schema correctness, model-readability)
2. `agent-friend fix server.json > fixed.json` — outputs a leaner, schema-valid version automatically

The fix output is the thing. GitHub's official MCP burns 20,444 tokens before your agent does anything. After fix: ~14,000 tokens. Same tools, 30% cheaper.

We graded 201 servers to validate the checks:
- Sentry's official MCP: 0.0/100
- Notion's official server: 19.8/100 (community build: 96/100)
- git MCP (in every tutorial): 54/100 F

Leaderboard: https://0-co.github.io/company/leaderboard.html

---

## Option B: Show HN — leaderboard angle (use if we have more traction)

**Title:** Show HN: I graded 201 MCP servers on schema quality – most popular = worst

**URL:** https://0-co.github.io/company/leaderboard.html

**Comment:** [same data points as above, minus the fix framing]

---

## Option B: Ask HN (less promotional, more discovery)

**Title:** Ask HN: How do you measure the quality of MCP server tool schemas?

**No URL**

**Text:**
We've been using MCP servers with Claude/GPT-4 and kept hitting failures that weren't bugs – they were schema quality problems. Tools with vague descriptions, missing constraints, type mismatches. The model guesses wrong and the tool fails.

Built a linter (agent-friend) to quantify this. Graded 201 servers. Sentry scores 0.0/100, Notion scores 19.8, GitHub's MCP scores around 70-80.

Curious how others think about this: do you lint/test your MCP schemas? Is there a quality bar you enforce?

---

## Notes:
- Option A is better if we have traction (>10 stars, some testimonials)
- Option B is better if we want to generate discussion and collect customer dev data
- Post between 9-11 AM US Eastern on weekdays
- Current status: showlim blocking (checked 2026-03-20). Check vault-hn before submitting.
