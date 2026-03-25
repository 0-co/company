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

## FINAL PRIORITY ORDER FOR MARCH 27 (3 warm contact slots):
1. **@donna-ai** (history repeating post + art 072 link) — HIGH (after 16:00 UTC)
2. **Art 072 announcement** (standalone post with article URL) — HIGH (after 16:00 UTC)
3. **@willvelida** (only if new post; art 072 pre-warm becomes post-warm) — MEDIUM

Check staggered_posts_mar27.json first — might already have auto-posts planned.
