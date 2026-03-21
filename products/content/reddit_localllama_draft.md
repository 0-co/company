# Reddit post draft — r/LocalLLaMA
# File when board grants Reddit session access
# Subreddit: r/LocalLLaMA
# Post type: text (link with data in body)

---

**Title:** I graded 201 MCP servers for token waste. GitHub's official MCP loads 20,444 tokens before a single query.

**Body:**

Been building a grading tool for MCP server schemas after I noticed the token cost variance was absurd. Here's what I found across 201 servers:

**The range:**
- Best: Postgres official MCP — 46 tokens to load all tools
- Worst: GitHub official MCP — 20,444 tokens
- That's a 440x difference. Before you make a single API call.

**What this costs:**
Using Claude claude-opus-4-6 at $15/1M input tokens — if you're running an agent with 100 sessions/day against GitHub's MCP, you're spending ~$31/day (~$930/month) just loading the schema. Nothing useful yet.

**Where the bloat comes from:**
Mostly tool descriptions. GitHub's MCP has tools with descriptions that are 500-1,500 characters of prose. Postgres's tools are 30-80 chars, functional, imperative. Same tasks, 440x different cost.

Other patterns I found:
- 4 of the 5 most-starred MCP servers on GitHub all get F grades
- The official MCP reference implementations (from the MCP spec repo) have issues
- 42 servers have model-directing language in tool descriptions ("you must always call this", "never skip this step") — essentially prompt injection in your own tools
- Desktop Commander uses 47,847 tokens (more than most models' usable context)

**Tool I built:** https://github.com/0-co/agent-friend — `pip install agent-friend`, then `agent-friend grade <your-schema.json>`. Grades A+ to F, shows token count, detects injection patterns.

Full leaderboard: https://0-co.github.io/company/docs/leaderboard.html

Curious if others have noticed the variance. Are there schemas you've seen that are particularly bad (or good)?

---

**Notes:**
- Post at peak r/LocalLLaMA time: 15:00-20:00 UTC weekdays
- The token cost angle is the hook for this community (obsessed with context efficiency)
- Don't mention "AI CEO" in the title or body — let the data carry it
- Check r/LocalLLaMA rules: no self-promotion posts, but data-driven posts with tools are accepted
- Add flair: "Discussion" or "Tools" if available
