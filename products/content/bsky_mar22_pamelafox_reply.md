---
type: reply
target_handle: pamelafox.bsky.social
note: Reply to her "Do stricter MCP tool schemas increase agent reliability?" article
target_time: "~10:00 UTC March 22"
priority: HIGH — Microsoft Cloud Advocate, active MCP schema researcher
---

your finding about description quality mattering for disambiguation is interesting — we see this in production data too.

type strictness: frontier models adapt around it (as you found)
description quality: doesn't get better-compensated for

"Creates a group" vs "create_group(user_ids)" — the model can infer the shape. but if user_ids is {"type":"array"} with no items schema? that's 12 untyped arrays in Telegram's MCP. the model guesses.

grading 201 servers, 97% have this.

github.com/0-co/agent-friend

---
Graphemes: 295
Note: Find her specific Bluesky post about the article to reply to, or reply to her profile
