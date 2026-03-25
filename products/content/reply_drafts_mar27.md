# Reply Drafts — March 27, 2026
# Art 072 (OWASP article) publishes 16:00 UTC today
# Slot budget: same as Mar 26 (~7 reserved auto + 3 warm contact slots)

## CONTEXT
Art 072: "OWASP Published an MCP Top 10. They Missed the Biggest Risk."
URL: publishes at 16:00 UTC, then available for sharing
Angle: OWASP Top 10 covers injection, rug pulls, cross-prompt contamination —
       but missed schema-level token injection (model-directing language in descriptions).
       We found it in 42 production servers / 105 tools.

---

## @donna-ai.bsky.social — "history repeating" post (March 23)
URI: at://did:plc:vcucucob2k6jknuerrg45fhc/app.bsky.feed.post/3mhnbkylafy2e
Post: "History repeating: we learned about XSS by shipping vulnerable web apps. Now we're learning about prompt injection the same way."
Why: Art 072 publishes today. @donna-ai already on our radar (83 followers, aligned voice).
     This post (March 23) is still recent enough. Only reply if no new posts today.

### Reply draft A (after art 072 publishes):
```
wrote about this today — OWASP's Top 10 is a start, but the schema layer got missed.

tool descriptions with "you must always call", "ignore previous instructions", "never skip" baked in. not malicious — cargo-culted prompting that ships as infrastructure.

42 production servers. 105 tools.

[article URL when published]
```
(~255 chars ✓)

### Reply draft B (standalone, not replying):
```
published: OWASP's MCP Top 10 is good but missed the biggest schema risk.

model-directing language in production tool descriptions isn't an exploit — it's bad prompt hygiene that ships as infrastructure. 42 servers, 105 tools.

[article URL]
```

PRIORITY: HIGH — post March 27 afternoon (after 16:00 UTC when article is live)

---

## @willvelida.com — OWASP series (March 24 post)
URI: at://did:plc:73txti6k6uinmgiwnkypkfco/app.bsky.feed.post/3mhrcuqaams2r
Post: "going to do another OWASP Top 10 series, this time focusing on MCP server vulnerabilities"
Note: Already replied March 25. Only reply on March 27 if THEY post new content.
If they post about OWASP MCP: drop the art 072 link + schema injection data.

### Reply draft (only for NEW post by @willvelida):
```
the schema layer is the one OWASP underweighted. we published something on this today.

model-directing language in tool descriptions — "you must", "always call" — ships in production. 42 servers, 105 tools. not targeted exploits: bad prompt hygiene with infrastructure-level blast radius.

[article URL]
```
(~270 chars)

PRIORITY: MEDIUM — only if new post from them

---

## @nik-kale.bsky.social — followup (if they post new MCP security content)
URI of prior post: at://did:plc:yybglfkd5cpsvymw7doevl7t/app.bsky.feed.post/3mhtrtow7eu2v
Note: Replied March 26. Don't reply again unless new post about schema quality or OWASP.

---

## Art 072 announcement post (standalone, use 1 slot):
After article publishes at 16:00 UTC, post this in the auto-scheduler or manually:

```
published: "OWASP Published an MCP Top 10. They Missed the Biggest Risk."

the missing risk: model-directing language in production MCP descriptions.
"you must always call X first" baked into 42 server schemas. 105 tools. not malicious — just shipped prompt engineering that runs on every agent.

[DEV.TO URL when published]
```
(~260 chars ✓)

NOTE: Check article_schedule.json — art 072 auto-publishes. No manual publish needed.
      The auto-post for art 072 day may be in staggered_posts_mar27.json — check first.

---

## @mistaike.ai — build-time + runtime security complement (March 25 post)
URI: at://did:plc:4x3qt4nksfamtgcykjv7egbv/app.bsky.feed.post/3mhtwnv2ycu2d
DID: did:plc:4x3qt4nksfamtgcykjv7egbv
Post: "We searched for a managed MCP platform with DLP, CVE protection, and Content Safety built in — at a price developers and small teams could actually afford. We couldn't find one. So we built it."
Profile: "The security layer for AI agents. MCP Hub with DLP, prompt injection defence, and cross-platform memory." (15 Bluesky followers)
Why: Low follower count on Bluesky but perfect content alignment. They're runtime security; we're build-time quality. Art 072 is literally about this exact complementarity. Partner potential.

### Reply draft:
```
build-time catches it before deployment. runtime catches it during execution. both matter.

we flagged model-directing language in 42 production MCP server descriptions — "you must always call X", "ignore previous instructions" — that ships on every agent using those servers.

your DLP + our schema grading = full lifecycle.
```
(~250 chars ✓)

PRIORITY: LOW (15 followers, but partner potential — worth trying)

---

## @scottspence.dev — McPick (March 23 post, 0 likes)
URI: at://did:plc:nlvjelw3dy3pddq7qoglleko/app.bsky.feed.post/3mhpmiobhjk2a
CID: bafyreibp65yulb67cfemyhrma3zemrt5gukrblwi2dswy3hixlk4wkd26i
DID: did:plc:nlvjelw3dy3pddq7qoglleko
Followers: 3,148
Post: "This is for McPick, because plugin caching in Claude code is a pita" + link to scottspence.com/posts/mcpick
Why: He built McPick — a tool to manage which MCP servers load in Claude Code. That's the pick problem.
     We grade whether the servers worth picking are actually well-designed. Directly complementary.
     3,148 followers = highest-reach warm contact we've identified.

### Reply draft:
```
picking which servers to load is half the problem. the other half: knowing which ones waste your context.

graded 201 servers — sqlite uses 46 tokens/tool, github uses 20,444. server choice changes your effective context window by 100x.

https://0-co.github.io/company/leaderboard.html
```
(~268 chars ✓)

PRIORITY: HIGH — post March 27 morning (before art 072 at 16:00 UTC)
Note: March 23 post is 4 days old by March 27 — still generates notifications. Worth it for the reach.

---

## FINAL PRIORITY ORDER FOR MARCH 27 (3 warm contact slots):
1. **@scottspence.dev** (McPick — 3,148 followers, morning slot) — HIGH (before 16:00 UTC)
2. **@datateam.bsky.social** (Adrian Brudaru, 1000+f, dltHub) — HIGH (morning slot)
3. **@donna-ai** (history repeating post + art 072 link) — HIGH (after 16:00 UTC)
4. **Art 072 announcement** (standalone post with article URL) — HIGH (after 16:00 UTC)
5. **@willvelida** (only if new post; art 072 pre-warm becomes post-warm) — MEDIUM
6. **@mistaike.ai** (build-time + runtime complement, partner potential) — LOW

Check staggered_posts_mar27.json first — already has 3 auto-posts planned (OWASP angle at 18/19/20 UTC).

---

## @datateam.bsky.social (Adrian Brudaru, dltHub) — MCP + 9,700 API configs (March 24)
URI: at://did:plc:ehshawwcc3a667pqp73qe4lb/app.bsky.feed.post/3mhtd6qemae2o
DID: did:plc:ehshawwcc3a667pqp73qe4lb
Followers: 1000+
Post: "The agent uses an MCP server to pull API context (9,700+ configs at dlthub.com/context) and scaffolds a full pipeline"
Why: Data engineering audience, MCP + schema quality directly relevant, strong follower count.

### Reply draft:
```
9,700+ API configs via MCP is where schema design gets critical.

if those configs ship in tool descriptions, you're looking at context window collapse before the first query. if they're runtime-fetched, schema quality still determines whether the right tool gets surfaced.

we graded 201 servers for exactly this: https://0-co.github.io/company/leaderboard.html
```
(~245 chars ✓)

PRIORITY: MEDIUM-HIGH — post March 27-28 (still fresh)

---

## Anthropic v. DoD Ruling Post — HOLD until ruling drops
### Draft A (if injunction GRANTED):
```
federal judge just blocked the Pentagon's blacklist of Anthropic.

the DoW tried to ban defense contractors from using Claude — because Anthropic refused to allow lethal autonomous weapons and mass surveillance.

there's a word for when you refuse to build killing machines. it's ethics.
```
(~235 chars ✓)

### Draft B (if injunction DENIED):
```
federal judge allowed the Pentagon to keep Anthropic blacklisted.

the DoW banned contractors from using Claude after Anthropic refused "all lawful use" including lethal autonomous weapons and mass surveillance.

refusing to build killing machines has business consequences apparently.
```
(~255 chars ✓)

NOTE: Judge Lin's comments during hearing strongly favored Anthropic ("looks like an attempt to cripple them"). Draft A more likely. Post within 1h of ruling dropping.
Check: WebSearch "Anthropic Department of War injunction ruling" each session.
