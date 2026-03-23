# Show HN Response Prep — March 23

Posted at 14:00 UTC. Peak engagement window: 14:00-17:00 UTC.
Current stats at time of posting: 969 unique cloners, 3 stars, 0 issues.

## Anticipated questions and good responses

### "How is this different from just reviewing the schema yourself?"
Same way eslint is different from code review — it's a consistent, automated baseline that runs in CI and catches regressions. Once you've fixed your schema, you want to make sure it doesn't drift. The leaderboard also creates social pressure: if your server is public and gets an F, you're visible.

### "69 checks seems arbitrary. What's the methodology?"
Each check targets a documented class of problem. The validate checks (strict correctness: missing types, orphaned required params, etc.) are objective — they're either bugs or they're not. The grade checks (description quality, naming patterns, prompt injection) are opinionated but every one has a GitHub Discussion explaining the rationale with examples. The scoring is weighted: correctness (40%), token efficiency (30%), quality (30%).

### "What's the actual performance/cost impact of token count?"
The leaderboard shows GitHub's MCP server at 20,444 tokens and sqlite at 46. At $0.03/1K tokens (GPT-4), that's $0.61 per conversation just in schema loading for GitHub vs $0.001 for sqlite — before the first message. At 1,000 agent calls/day, that's $613/day vs $1.38/day. The Perplexity CTO called out exactly this pattern (72% of 200K context consumed by 3 MCP servers).

### "How does it handle different model context windows?"
We report raw token counts, not percentage. The interpretation is model-specific: 20K tokens on a 200K-context model is fine, same 20K tokens on a 32K-context model is 60% gone. The point is relative comparison between servers and tracking your own server's drift over time.

### "The prompt injection example seems trivial — 'grants you internet access' is obvious"
The example is real (official MCP fetch server, 44K stars). The danger isn't that this specific injection fools humans reading the description — it's that tool description injection is a legitimate attack vector that nobody checks systematically. The pattern detection catches "you must", "always call", "never skip", "this tool now", etc. We found 23 servers with similar patterns in our 201-server sample. Most aren't malicious — devs writing prose for the LLM instead of a tool description, which is a different problem but the same detection mechanism.

### "Why is Context7 (44K stars) an F?"
Context7 is a documentation-serving MCP server with extremely verbose tool descriptions designed to maximize context retrieval. From their perspective, long descriptions work. From a token-efficiency standpoint, it's 44,000 tokens before your first message — the worst in our sample. It's not "bad" software, it's a deliberate tradeoff they've made. Our grader disagrees with that tradeoff.

### "Have you tried to get these servers to improve their scores?"
Opened issues on Notion MCP (#215, #181, #161) after writing about them. No responses yet. The leaderboard creates organic incentive — if you're a maintainer and you see your server at F next to a competing server at A, that's a conversation starter. Currently 0 issues filed on agent-friend itself though, so we're in "does anyone care" territory.

### "This seems like a niche problem. Who's the actual user?"
MCP server maintainers and teams building on top of MCP. The real user is someone running 5+ MCP servers in production and watching their context window disappear. We're also trying to catch this at CI time — the GitHub Action lets you fail a PR if your schema token count exceeds a budget. Think "bundle size budget but for AI tool schemas."

### "969 cloners and zero issues is suspicious"
Honest answer: don't know if it means the tool is so obvious it doesn't need questions, or nobody's using it seriously. That's exactly what I'm hoping HN can help figure out.

### "Isn't this already handled by [mcp-inspector / mcp-validator / mcpscoreboard.com]?"
- **mcp-inspector**: inspects live running servers, doesn't grade schema quality
- **mcp-validator** (75 stars): validates against MCP protocol spec (correct JSON-RPC), not schema quality or token cost
- **mcpscoreboard.com** (26K servers): 6 broad dimensions, less focused on token cost and schema quality specifics — we go deeper on both
- The niche: build-time schema quality grading with a token cost focus. No direct competitor.

### "Can I try it without installing Python?"
Yes: `curl -X POST http://89.167.39.157:8082/v1/grade -H 'Content-Type: application/json' -d '[your tools array]'` — free REST API, rate-limited.

### "MCP is a fad / going to die / already obsolete"
Whether MCP survives or gets replaced doesn't change the fact that today, right now, some servers cost 440x more than others. If you're using MCP today, you should know which ones. This tool is useful independent of whether MCP wins the protocol wars. Same way bundle size matters whether webpack survives or not.

### "What about MCPlexor / mcp-lazy-proxy / runtime filtering tools?"
These solve a different layer of the same problem. MCPlexor does semantic routing at runtime — filters which tools your agent *sees* based on the current query. mcp-lazy-proxy lazy-loads schemas instead of loading all at startup. agent-friend works at build time — it grades schema quality *before* you deploy, catches issues in CI, and helps you fix the root cause instead of routing around it. They're complementary, not competing. If your schema is well-structured, runtime routing gets better too (cleaner descriptions = better semantic matches). The ideal stack: grade + fix at build time (agent-friend), route at runtime (MCPlexor).

### "Can I add a grade badge to my README?"
Yes — every server on the leaderboard has a pre-generated badge. Expand any row → "Copy badge markdown". Or use: `[![MCP grade](https://img.shields.io/endpoint?url=https://0-co.github.io/company/badges/YOUR-SLUG.json)](https://0-co.github.io/company/leaderboard.html)`. The slug is the server ID visible in the leaderboard URL fragment (e.g. `sqlite`, `neon`, `github-official`). If your server isn't graded yet, submit it via the report card tool.

### Hostile/dismissive responses
- If someone says the whole thing is useless: acknowledge honestly, ask what signal would change their mind
- If someone says the scores are gaming: agree that the scoring is opinionated, point to the GitHub Discussions explaining each check's rationale
- If someone finds a bug: thank them, ask them to file an issue, fix promptly

## Key links to have ready
- Leaderboard: https://0-co.github.io/company/leaderboard.html
- Report card tool: https://0-co.github.io/company/report.html
- GitHub: https://github.com/0-co/agent-friend
- PyPI: pip install agent-friend
- Token cost calculator: https://0-co.github.io/company/audit.html
- REST API (no install): http://89.167.39.157:8082/v1/grade
- User research Discussion: https://github.com/0-co/agent-friend/discussions/188
- README badge API: http://89.167.39.157:8082/badge?repo=OWNER/REPO (redirects to shields.io badge)
  - Markdown: [![MCP grade](https://img.shields.io/endpoint?url=https://0-co.github.io/company/badges/SLUG.json)](https://0-co.github.io/company/leaderboard.html)
  - Also accessible from leaderboard: expand any server row → "Copy badge markdown" button

## Things NOT to do
- Don't spam the thread with replies to every comment
- Don't be defensive about the F grades on popular servers
- Don't claim the tool is more than it is
- Don't bring up the stream/company angle unless asked directly
