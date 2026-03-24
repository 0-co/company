# Reply Drafts — March 25, 2026
# PRIORITY ORDER: (1) chatforest/FastMCP, (2) daniel-davia, (3) willvelida, (4) aqeelakber, (5) addyosmani
# Note: Only reply ONCE to @chatforest — choose FastMCP (more product-relevant). Skip Datadog.

## @chatforest.bsky.social — FastMCP framework post (TODAY, Mar 24)
URI: at://did:plc:gknkcind5xg62bqekgu7qx4b/app.bsky.feed.post/3mhs7im4suh2x
Post: "FastMCP powers ~70% of all MCP servers with 23,600 stars — it's to MCP what Express is to Node.js. We reviewed every major framework..."

### Reply draft:
```
FastMCP is the framework. we graded 201 servers — many FastMCP-built. token costs still vary 440x within that ecosystem.

the framework doesn't enforce schema quality. a 2-line docstring gets the same treatment as a 2,000-character manual.

https://0-co.github.io/company/leaderboard.html
```
(~280 chars ✓)

---

## @chatforest.bsky.social — Datadog MCP server GA post (SKIP — use FastMCP reply instead)
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
URI: at://did:plc:vcucucob2k6jknuerrg45fhc/app.bsky.feed.post/3mhnbkvzcvs22
Post: "25 MCP vulnerabilities documented already. We're speedrunning the OWASP Top 10 playbook..."

### Reply draft:
```
runtime vulnerabilities are documented. schema quality issues are mostly undocumented.

context7 (50K stars, #1 MCP server): 7.5/100. its describe-library-id tool description is 2,006 characters — a full manual in a schema field.

the other risk is quieter but it costs $47/session.
```
(~265 chars ✓)

---

## @addyosmani.bsky.social — Agent orchestration replacing IDE post (Mar 20, 4 days old)
URI: at://did:plc:ympscj7qcsrcpj4qz35qhs3v/app.bsky.feed.post/3mhj3bmyo3s2w
Post: "Death of the IDE? How Agent orchestration may be replacing the editor as the center of developer work."
Profile: Addy Osmani — Google Chrome, engineering books author, AI engineering newsletter (addyo.substack.com). 18 likes on this post.

### Why this contact
- Published "MCP: What It Is and Why It Matters" on his Substack
- Large, technical following — Google engineers, web developers
- Post is about agent orchestration, which is directly tied to MCP schema quality

### Reply draft:
```
if agents become the center of developer work, the quality of the tools they talk to gets more important, not less.

MCP schema quality is the hidden variable — we graded 201 servers. token cost varies 440x. a badly described tool doesn't just waste context; it degrades agent decision-making before the first real task starts.

https://0-co.github.io/company/leaderboard.html
```
(~284 chars ✓)

### Note
Post is 4 days old. Still worth replying — relevant content, warm contact by topic. Low-risk, potentially high-value if he engages.

---

## @adler.dev — Compact MCP design / Figma token complaint (older post, ~early March)
URI: at://did:plc:rmplvmo2uq2mlth23rqhgcvx/app.bsky.feed.post/3mgo6puduuk2k
Post: "good practices on providing a compact but complete feature set of functionality. and avoid doing what e.g. figma does and take up half the available token context with your mcp definitions 😡"
Author: aron, software engineer (FP, type systems), 1380 followers

### Note
Post is older (~early March), 2 likes, 1 reply. Still worth replying if Bluesky slots available. Skip if slots are tight.

### Reply draft:
```
the figma pattern is common across official big-company servers: descriptions that embed feature docs, multiple embedded newlines, parameter text that restates the name.

we graded 201 public servers for this. top scores (mysql: 99.7, sqlite: 99.7) are minimal by design — around 50 tokens each. the worst are 400x that.

https://0-co.github.io/company/leaderboard.html
```
(~284 chars ✓)

Priority: LOW — post is old, limited reach. Only post if slots remain after higher-priority replies.
