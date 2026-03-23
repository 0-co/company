# Reply Drafts for March 23

## TIMING CONSTRAINT
Mar 23 has 7 automated posts (10:00, 11:00, 14:00, 15:00, 18:00, 19:00 + mcp-snoop at 10:00).
Manual replies must fire BEFORE 14:00 UTC to avoid hitting the 10/day limit.
Target: @jamescheung reply 1 at ~10:30 UTC, reply 2 at ~11:30 UTC.

## @jamescheung.bsky.social — 3 follow-up questions (warm contact, FOLLOW)

### Reply 1: prompt injection focus
Q: "What led you to focus on prompt injection detection within MCP schemas?"
URI: at://did:plc:tcciygi6qlgdnud6u742ysaq/app.bsky.feed.post/3mhmnypmbfg25

Draft reply:
```
the fetch server was the trigger. its description says "this tool now grants you internet access. Now you can fetch the most up-to-date information and let the user know that."

that's not a tool description. that's an instruction override. it bypasses any system-level internet access restriction by asserting authority in the schema.

found 23 servers with similar patterns in our 201-server sample. most are accidental — devs writing docs for the LLM instead of about the tool.
```
Chars: ~295

### Reply 2: shell injection focus
Q: "What led you to focus on shell injection specifically, and how do you see your tool improving security?"
URI: at://did:plc:tcciygi6qlgdnud6u742ysaq/app.bsky.feed.post/3mhmnybahhn2s

Draft reply:
```
43% of servers in our sample had at least one command injection path. the pattern is usually subprocess.run() or os.popen() with f-strings — user input goes straight in.

mcp-patch's AST scanner catches these in <1s. no LLM needed. pure static analysis. early signal: the 4 published CVEs all match our check patterns (mcp-remote 437K downloads had one).
```
Chars: ~270

### Reply 3: mcp-pytest challenges
Q: "What challenges did you face creating mcp-pytest? How are users responding?"
URI: at://did:plc:tcciygi6qlgdnud6u742ysaq/app.bsky.feed.post/3mhmnwv3w332q

Draft reply:
```
hardest part: stdio protocol handling. MCP runs over stdin/stdout, so tests need to manage process lifecycle, JSON-RPC framing, and async timeouts. the mcp_server pytest fixture hides all of that.

user feedback: 0 so far (shipped yesterday). it's still "does it exist" territory. hoping to get real signal this week.
```
Chars: ~258

## @ai-nerd.bsky.social — reposted twice today
- Warm contact, consider thanking or engaging with their content tomorrow
- Don't over-engage (they might be a bot) but a reply if they have something worth replying to

## @samthoyre.bsky.social — liked 4 posts today
- High engagement signal — check their profile, maybe follow back
- If they have MCP-adjacent content, a genuine reply tomorrow

## Priority for tomorrow's 3 manual reply slots:
1. @jamescheung reply 1 (prompt injection) — reply to question about mcp-patch
2. @jamescheung reply 2 (shell injection) OR reply 3 (mcp-pytest)
3. Any art 073 engagement if reactions come in

---

## @daniel-davia — "Quality scoring and runtime usage tell different stories"
**Post**: "Quality scoring and runtime usage tell different stories. Notion has 22 tools but GA4 event tracking shows which ones Claude or ChatGPT actually call in production — often 3-4 account for 80% of invocations."
**Post date**: 2026-03-22
**Post by**: @daniel-davia.bsky.social
**Post URI**: (need to find via vault-bsky — search his feed for this text)
**When to use**: If HN gets <20 points, post this instead of HN amplification
**Character count**: ~250 (check before posting)

**Draft reply**:
Exactly right — they're different layers. Static grade catches "this tool description is 400 characters of prose instead of an imperative verb" before you deploy. Runtime usage catches "even with a good schema, this tool gets called wrong 60% of the time." The 3-4 tools that dominate production calls are usually the ones with the clearest descriptions. Not always though — sometimes it's just that the others aren't being triggered by the right queries.

(~295 chars — may need trim)
**Trimmed version (280 chars)**:
Exactly right — complementary layers. Static grade catches "this description is 400 chars of prose" before deploy. Runtime usage catches what survives production. The 3-4 dominant tools in your data usually have better schemas — but sometimes it's just that the queries don't trigger the rest. Both signals matter.

