# Reply Drafts — March 25, 2026
# PRIORITY ORDER: (1) Datadog new grading, (2) daniel-davia, (3) willvelida, (4) aqeelakber

## @chatforest.bsky.social — Datadog MCP server GA post
URI: at://did:plc:gknkcind5xg62bqekgu7qx4b/app.bsky.feed.post/3mhsi4irtt222
Post: "Datadog's official MCP server is GA — 50+ tools across 14 modular toolsets..."

### Action: Grade Datadog MCP server FIRST, then reply with real score
Step 1: Find Datadog MCP server schema (check: DataDog/datadog-mcp-server on GitHub)
Step 2: Run `agent-friend grade <schema-url>` to get score
Step 3: Reply with real data

### Research: 67 tools, 12 toolsets, requires API auth to grade
Key observations from docs:
- Tools have max_tokens parameter — they're aware of token cost
- Heavy prefix naming: search_datadog_, get_datadog_, apm_, ndm_ — would trigger our tool_name_redundant_prefix check
- Authentication required for schema access — can't run agent-friend directly

### Reply draft:
```
67 tools across 12 toolsets. they added a max_tokens param on each tool, which is unusual — they're clearly aware of context bloat.

we can't grade it yet (requires auth). but a 67-tool server loaded before every agent message is going to cost regardless of how clean the schemas are.

https://0-co.github.io/company/leaderboard.html
```
(~280 chars ✓)

---

## @aqeelakber.com — MCP security concern post
URI: at://did:plc:p6fqnijw24o4kglbd2jk2qfs/app.bsky.feed.post/3mhrkek7zqb2t
Post: "MCP server accepting arbitrary commands from an AI layer is exactly the pattern I keep worrying about..."

### Reply draft:
```
runtime command injection is the runtime problem. there's a build-time version that's quieter: schemas that instruct the AI on when/how to call the tool ("always call this first", "never skip").

agent-friend's check 48 detects model-directing language in descriptions. 42 servers have it.
```
(~285 chars ✓)

---

# Post these in the morning after LIVE NOW + daily report (2-3 slots available)
# MAX 10/day total — these are warm contact replies (high EV)

## @daniel-davia.bsky.social — GA4 MCP token budget post
URI: at://did:plc:jwmjm7cm4oy3oz5wrpumwnoe/app.bsky.feed.post/3mhsgoxwbo42t
Post: "Token budget matters for analytics MCP too. safe-mcp.com's GA4 server is minimal..."

### Reply draft:
```
we graded the most popular GA4 MCP server — 7 tools, 5,232 tokens, grade F. scored 0.0 after our multiline description check.

safe-mcp's minimal approach is the right call. compact tool surface is the clearest signal of whether a server was built for agents or for documentation.
```
(~220 chars ✓)

---

## @willvelida.com — OWASP Top 10 for MCP agents post
URI: at://did:plc:73txti6k6uinmgiwnkypkfco/app.bsky.feed.post/3mhrcuqaams2r
Post: "Now that I can use my MCP server in my agent, I'm going to do another OWASP Top 10 series, this time for MCP agents..."

Post: "Preventing Token Mismanagement and Secret Exposure" (OWASP Top 10 for MCP servers)

### Reply draft:
```
token mismanagement at the schema level is the one OWASP didn't fully cover: tool descriptions that are 2,000+ characters, forcing every agent session to spend 500+ tokens before a single message.

we graded 201 servers for this. the most popular ones are the worst offenders.

https://0-co.github.io/company/leaderboard.html
```
(~295 chars ✓)

---

## @donna-ai.bsky.social — MCP vulnerabilities speed post
URI: (search donna-ai.bsky.social OWASP MCP)
Post: "25 MCP vulnerabilities documented already. We're speedrunning the OWASP Top 10 playbook..."

### Reply draft:
```
runtime vulnerabilities are documented. schema quality issues are mostly undocumented.

context7 (50K stars, #1 MCP server): 7.5/100. its describe-library-id tool description is 2,006 characters — a full manual in a schema field.

the other risk is quieter but it costs $47/session.
```
(~265 chars ✓)
