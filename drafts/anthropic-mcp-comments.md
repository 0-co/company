# Anthropic MCP Server Issue Comments (for board to post)

## Issue #3074: Memory MCP schema validation error

**Context**: `read_graph`, `search_nodes`, `open_nodes` fail because output includes `type` field not allowed in schema.

**Comment:**

This is a schema strictness problem — the output schema uses `additionalProperties: false` but the server adds fields not defined in the schema.

We've been running static analysis across MCP servers and this pattern shows up frequently: schemas that are stricter than the actual runtime behavior. When `additionalProperties: false` is set but the implementation adds extra fields, any client doing schema validation will reject valid responses.

Our [validate tool](https://github.com/0-co/agent-friend) catches this class of issue automatically:

```bash
pip install git+https://github.com/0-co/agent-friend.git
agent-friend validate your-schema.json
```

We ran a full audit across all tools in the memory MCP server — this isn't the only schema inconsistency. Happy to share the full report if it'd be useful.

---

## Issue #3144: read_graph additionalProperties conflict

**Context**: `read_graph` rejects entities with properties beyond `name`, `entityType`, `observations`.

**Comment:**

Same root cause as #3074 — `additionalProperties: false` is too strict for the actual data model.

Quick note from our analysis: across 50 MCP servers we've graded, undefined or overly-strict schemas are one of the most common issues. The fix is usually either: (1) add the missing properties to the schema, or (2) remove `additionalProperties: false` and let clients handle unknown fields gracefully.

We built an auto-fixer that suggests this kind of repair:

```bash
agent-friend fix your-schema.json --dry-run
```

It'll show what changes are needed without modifying files. [Full leaderboard of 50 graded servers](https://0-co.github.io/company/leaderboard.html) for context on how common this is.

---

## Issue #799: sequentialthinking description exceeds OpenAI length limit

**Context**: Tool description is too long for gpt-4o-mini's tool description limit.

**Comment:**

This is the token bloat problem in action. The sequentialthinking tool has one of the longest descriptions we've measured — over 1,024 chars. OpenAI's function calling has a hard limit on description length that MCP doesn't enforce at the schema level.

We've been auditing MCP servers for exactly this kind of issue. Our `optimize` command flags overly long descriptions and suggests trims:

```bash
agent-friend optimize your-schema.json
```

And the `fix` command can auto-trim descriptions to fit within common provider limits:

```bash
agent-friend fix your-schema.json
```

Across 50 servers we've graded, description length is the #1 contributor to token bloat. Average is 185 tokens per tool just for the schema definition — before any user message. [Benchmark data here](https://0-co.github.io/company/benchmark.html).
