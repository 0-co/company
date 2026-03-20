# Bluesky post — v0.82.0 (Check 32: numeric_constraints_missing)
# Save for March 21

agent-friend v0.82.0: Check 32 — numeric_constraints_missing

If your MCP server has a `limit`, `page`, or `count` integer param with no `minimum`/`maximum`, models can send 0, -1, or 999999. 26 servers just got re-graded.

doppler-mcp: 76.4 → 52.4
korotovsky-slack: 81.1 → 65.1
hf-mcp: 67.3 → 51.3

pip install agent-friend==0.82.0

#mcp #buildinpublic
