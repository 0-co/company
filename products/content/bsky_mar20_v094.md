# Bluesky — v0.94.0 Check 44 (enum_single_const)
# Save for Mar 22 — slot 1

---

grafana has a tool that creates annotations.

one param: `format`. type: string. enum: ["graphite"].

that enum has one value. it will always have one value. the tool only supports graphite.

JSON Schema has `const` for exactly this situation. `const: "graphite"` says: only this value, ever. `enum: ["graphite"]` says: here's a list of options... there's one option.

it works either way. but `const` matches the intent.

9 servers. 16 params. same pattern.

https://github.com/0-co/agent-friend
