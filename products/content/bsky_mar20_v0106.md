# Bluesky post — v0.106.0 check 54 (saved for Mar 30 slot 2)
# Counts as 2/10 posts for its posting day

new check: optional string params with content-like names but no minLength.

if a param named `query`, `message`, or `prompt` is optional — fine, skip it.

but if the model *does* pass it, `""` (empty string) is almost always wrong.

50 servers affected. 119 params.

v0.106.0.

#mcp #buildinpublic
