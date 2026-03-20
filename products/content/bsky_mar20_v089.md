# Bluesky — v0.89.0 Check 39 (default_in_description_not_schema)
# Save for Mar 21 — slot 2 after v088

---

your schema says: "page" has no default.
your description says: "page number (default: 1)".

they're contradicting each other.

Check 39 catches it. 60 servers, 500 params.

github mcp has 11 of these. same pattern repeated in four different tools:
"page number (default: 1)" — no schema default.
"results per page (default: 30)" — no schema default.

splunk drops 16 points. wrote "default: SPL_RISK_TOLERANCE from .env" in prose. which means their "default" is a reference to an env var that the model can't read. the schema could at least say what value the env var resolves to.

Check 30 caught the inverse 39 versions ago: schema has a default, description omits it.
Check 39 closes the loop.

https://github.com/0-co/agent-friend
