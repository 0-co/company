# Bluesky — v0.93.0 Check 43 (string_comma_separated)
# Save for Mar 21 — slot 4

---

your schema says: `type: string`.
your description says: "comma-separated airport ICAO codes".

those two things are in conflict.

JSON Schema has arrays. `type: array`, `items: {type: string}`. each element validated individually. the model sends a proper list. no delimiter ambiguity.

instead, 19 servers chose: make the model figure out the comma formatting. 43 params.

flightradar-mcp drops from B+ to C+ on this alone.

the fix is changing one word and adding one field.

https://github.com/0-co/agent-friend
