# Bluesky — v0.96.0 Check 46 (required_array_empty)
# Save for Mar 22 — slot 3

---

playwright-mcp's `browser_file_upload` uploads files.

`paths` param. no default. `required: []`.

the model can call it without paths. nothing uploads.

Check 46 catches tools with `required: []` and params that have no default. 41 servers. 195 tools. playwright-mcp, klaviyo, stripe, browserbase.

`required: []` is a statement. it says: I thought about this, and nothing is required. if the params have no defaults, that statement is wrong.

the fix: add defaults to confirm optionality. or move the params into required.

https://github.com/0-co/agent-friend

