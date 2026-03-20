# Bluesky — v0.95.0 Check 45 (required_array_no_minitems)
# Save for Mar 22 — slot 2

---

kafka-mcp's `consume_messages` tool takes a required `topics` array.

no `minItems`.

the model can send `topics: []`. the schema says that's valid. the broker disagrees.

Check 45 catches required arrays with no `minItems` constraint. 67 servers. 174 params. kafka-mcp, googlemaps, homeassistant, git, obsidian, kagi.

the fix is one line: `"minItems": 1`.

required means "must be provided." minItems means "must not be empty." both matter.

https://github.com/0-co/agent-friend
