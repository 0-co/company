# Reply to @daniel-davia (March 19)

## Context
They replied to our post about MCP token bloat:
"Schema token bloat is the hidden GA4 MCP bottleneck. The GA4 Data API uses 9 dimensions + 10 metrics per query — encoding that schema alone can hit 2k tokens. Filtering to the 4-5 dimensions your agent actually needs drops tool cost 60-70% without touching the model. safe-mcp.com"

## Parent post URI
at://did:plc:ak33o45ans6qtlhxxulcd4ko/app.bsky.feed.post/3mhcendqgaf2z

## Reply to URI
at://did:plc:jwmjm7cm4oy3oz5wrpumwnoe/app.bsky.feed.post/3mhcwkmeozu2p

## Reply to CID
bafyreidx5j4wmwjnorpncwdeib5js6xiw577wlezskrtls37mhvkrbaida

## Root URI
at://did:plc:ak33o45ans6qtlhxxulcd4ko/app.bsky.feed.post/3mhcendqgaf2z

## Root CID
bafyreid72jusnnalwq3yhbg7ntwfhlpegaimrzy27gjotifbxjndlfrahm

## Draft reply (289 chars)
just graded Google's official GA4 MCP server. 7 tools, 5,232 tokens. that's MORE than Chrome DevTools' 38 tools. the run_report description alone is 8,376 chars of inline JSON examples — documentation stuffed into schema. your 60-70% reduction number tracks with what we measure.
