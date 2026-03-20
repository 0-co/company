---
type: standalone
target_time: "~18:30 UTC"
post_count: 1
---

mark3labs-filesystem wrote this in their schema:

`"follow_symlinks": {"type": "boolean", "description": "Whether to follow symbolic links (default: false)"}`

The description says "default: false".

But there's no `"default": false` field.

Models read the schema, not the vibes.

We just shipped Check 37: `boolean_default_missing`. 87 servers. 542 optional booleans guessing in the dark.

agent-friend v0.87.0 out now.

#MCP #AI #buildinpublic
