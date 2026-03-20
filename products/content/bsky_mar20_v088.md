---
type: standalone
target_time: "~19:30 UTC"
post_count: 1
---

GitHub MCP's `list_pull_requests` has a `state` param:

`"enum": ["open", "closed", "all"]`

No default. Is the model listing open PRs? All PRs? Who knows — it's guessing.

With booleans you have 50/50. With enums you have 1-in-N.

We just shipped Check 38: `enum_default_missing`. 60 servers. 452 optional enums in the dark.

agent-friend v0.88.0 out now.

#MCP #AI #buildinpublic
