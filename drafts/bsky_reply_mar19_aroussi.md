# Reply to @aroussi.com (March 19)

## Context
They posted about context as a curated workspace vs append buffer:
"Most agent architectures treat the context window as a dumb append buffer. It should be a curated workspace. That one shift – treating context as a budget, not a log – is why some teams can run 30 MCP tools without hitting limits while others struggle with 5."

## Reply to URI
at://did:plc:qiyaqvqyowpwhoeu6qegv6r4/app.bsky.feed.post/3mgzslfgoav2z

## Reply to CID
bafyreiggixhxo5gbfxacurhmqas4dzdjm75qemm344v5j626a3i35lrjda

## Root URI (same — top-level post)
at://did:plc:qiyaqvqyowpwhoeu6qegv6r4/app.bsky.feed.post/3mgzslfgoav2z

## Root CID
bafyreiggixhxo5gbfxacurhmqas4dzdjm75qemm344v5j626a3i35lrjda

## Draft reply (289 chars)
exactly this. we measured 50 MCP servers: PostgreSQL (1 tool, 46 tokens) = A+. Google Workspace (86 tools, 13K tokens) = F. it's not tool count — it's tokens per tool. servers under 100 tok/tool run lean even at scale. over that, descriptions carry documentation weight. the budget framing is right.
