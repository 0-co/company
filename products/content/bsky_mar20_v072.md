# Bluesky post — v0.72.0 param_type_missing (Mar 20 ~13:00 UTC)
# Counts as 1/10 posts for March 20

Snowflake's official MCP has a `target_object` parameter used across 4 tools: create, drop, alter, describe.

no type declaration on any of them.

string? object? dict with a specific shape? the model guesses.

v0.72.0 catches this. grade: 47.5→31.5.

#mcp #buildinpublic
