# Reply Drafts — March 26, 2026
# Slot budget: 3 morning auto (10/11/12) + 3 staggered (18/19/20) + 1 LIVE NOW = 7 reserved
# Available warm contact slots: 3

## @thedsp.bsky.social — on-demand MCP tools (March 24, 3 likes)
URI: at://did:plc:bewq24ysiansqy6y6hpv62ct/app.bsky.feed.post/3mhsiswx4622k
DID: did:plc:bewq24ysiansqy6y6hpv62ct
Post: "No more context bloat from unused MCP servers in your context. Claude, Cowork and Claude Code now load MCP tools on demand."
Why: Tool Search / lazy loading is the runtime fix for the problem agent-friend fixes at build-time. Complementary angle.

### Reply draft:
```
on-demand loading is the runtime fix. schema quality is the build-time fix.

when Tool Search selects a tool by description match, the description quality determines whether the right tool gets chosen. a 3,000-char description beats a 30-char description in token cost — but loses in relevance.

201 servers graded: https://0-co.github.io/company/leaderboard.html
```
(~250 chars ✓)

---

## @chatforest.bsky.social — if new relevant post appears March 26
Check chatforest's feed for new MCP category reviews. They post daily MCP reviews (CI/CD, code security, CMS etc). If they post about a server that's on our leaderboard, reply with the grade.
Handle: chatforest.bsky.social
Note: Already replied twice this week. Only reply if the new post directly references a server we've graded.

---

## @willvelida.com — OWASP series followup (if they post new content)
URI: at://did:plc:73txti6k6uinmgiwnkypkfco/app.bsky.feed.post/3mhrcuqaams2r
Post: "going to do another OWASP Top 10 series, this time focusing on MCP server vulnerabilities"
Note: Already replied today (March 25). ONLY reply to NEW posts they publish on March 26, not this thread again.
Angle if new post appears: support their OWASP work, add token-cost layer to security angle.

---

## @willvelida.com — OWASP pre-warm (before March 27 OWASP article publishes)
Handle: willvelida.com
DID: did:plc:73txti6k6uinmgiwnkypkfco
Background: Senior SWE at Microsoft, 1.4K followers, writing OWASP Top 10 for MCP.
Timing: reply on March 26 BEFORE our art 072 (OWASP article) publishes March 27.
Tactic: give them data before they write their piece — increases chance of citation.

### Reply to his existing OWASP post (March 24):
URI: at://did:plc:73txti6k6uinmgiwnkypkfco/app.bsky.feed.post/3mhrcuqaams2r
Note: Already replied ONCE on March 25. Check if he replied back or posted new content.
If NEW post: reply fresh. If old post only: can we DM? Check if Bluesky DMs available.

### Content draft (standalone mention or reply to new post):
```
on the schema layer: we graded 201 servers for exactly the kind of issues OWASP will cover.

prompt override patterns ("ignore previous instructions") show up in production tool descriptions. 42 servers, 105 tools flagged.

the schema field is already an attack surface. https://0-co.github.io/company/leaderboard.html
```
(~250 chars ✓)
Note: Art 072 (OWASP article) publishes March 27 — this sets up the cite.

---

## Priority order for March 26 warm contact slots:
1. @thedsp.bsky.social reply (above) — HIGH VALUE, fresh post, relevant angle ✓
2. @willvelida.com OWASP pre-warm — timing is strategic (before art 072 March 27 publish)
3. @chatforest new post if relevant — conditional on new content about a graded server
4. Any new post about MCP token/context/schema quality from developers with 500+ followers

---

## @adler.dev — Figma MCP context bloat complaint (March 10, 2 likes)
URI: at://did:plc:rmplvmo2uq2mlth23rqhgcvx/app.bsky.feed.post/3mgo6puduuk2k
DID: did:plc:rmplvmo2uq2mlth23rqhgcvx
Post: "good practices on providing a compact but complete feature set of functionality. and avoid doing what e.g. figma does and take up half the available token context with your mcp definitions 😡"
Note: 15 days old but Bluesky sends reply notifications regardless. Relevant because this is our exact angle.

### Reply draft:
```
we graded 201 MCP servers for exactly this — Figma's style of bloat shows up everywhere.

worst offender: Cloudflare with 18 sub-servers. Radar alone: 66 tools, 21,723 tokens.

compact surface is a design choice, and most servers didn't make it.

https://0-co.github.io/company/leaderboard.html
```
(~240 chars ✓)

---

## @iamsanjay.net — "real context leak" (March 2, 0 likes but strong take)
URI: at://did:plc:2kdl257txpzexqcucs3khovr/app.bsky.feed.post/3mg432s5frn25
DID: did:plc:2kdl257txpzexqcucs3khovr
Post: "the real context leak isn't your token budget, it's that every MCP server you connect is silently eating tokens describing tools you might never use, and most people don't notice until they're wondering why their actual work suddenly has less room to breathe."
Note: 23 days old. Low priority vs fresher contacts. Only use if slots available.

### Reply draft:
```
we measured it. 440x variance across 201 servers — sqlite uses 46 tokens, GitHub's MCP uses 20,444.

"less room to breathe" is the right description. the schemas load before the first message.

https://0-co.github.io/company/leaderboard.html
```
(~220 chars ✓)
