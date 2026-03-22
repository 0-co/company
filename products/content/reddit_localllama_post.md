# Reddit Post — r/LocalLLaMA

**Title:** GitHub's MCP server costs 20,444 tokens to load. Postgres: 46 tokens. Built a grader to catch this.

**Subreddit:** r/LocalLLaMA

**Body:**

If you're running local LLMs with MCP tools, the token overhead from bad schemas is destroying your context window before the model does anything useful.

Examples from grading 201 real MCP servers:

| Server | Load cost |
|--------|-----------|
| Postgres MCP | 46 tokens |
| SQLite MCP | 47 tokens |
| GitHub MCP | 20,444 tokens |
| Cloudflare MCP | ~35,000 tokens |

That GitHub number is real. 200+ tools, each with massive descriptions that could be 90% shorter without losing information.

For local models with 4K-8K context windows, loading GitHub MCP essentially fills your context with schema overhead. You've got maybe 10-20% of your window left for actual conversation.

I built **agent-friend** to grade this: https://github.com/0-co/agent-friend

```
pip install agent-friend
agent-friend grade schema.json
```

Outputs letter grade A+ to F, specific issues, and an `optimize` command that strips the bloat while preserving the semantics.

Also detects prompt injection patterns in tool descriptions — people are embedding `ignore previous instructions` in MCP schemas. We catch that.

`pip install agent-friend`

---
Notes: r/LocalLLaMA skews practical/quantitative. Lead with the token numbers. Make the local LLM angle clear.
