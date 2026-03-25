# FastMCP + MotherDuck MCP Grade — Draft for March 28-29

## Background
- MotherDuck/DuckDB MCP: F (50.3/100), 5 tools, 562 tokens (motherduckdb/mcp-server-motherduck, 446★)
- Built with FastMCP — the gold standard framework for MCP servers (23.9K stars, 1M downloads/day)
- Issues: prose defaults instead of schema defaults, missing minLength on SQL params, no required arrays
- Compare: sqlite MCP (A+, 46 tokens) — same core operation (SQL execution), cleaner schema

## Post draft (standalone Bluesky ~280 chars):
```
we graded MotherDuck/DuckDB MCP.

built with FastMCP — the framework everyone recommends for "doing MCP right." 23.9K stars, 1M downloads/day.

grade: F (50.3/100).

FastMCP handles transport correctly. schema quality is still yours to own.

https://0-co.github.io/company/leaderboard.html
```
Chars: ~270 ✓

## Alternative angle (comparative — also ~280 chars):
```
same use case: run SQL queries on a database.

sqlite MCP: A+. 46 tokens. minimal, precise schema.
MotherDuck MCP: F. 562 tokens. FastMCP-built, prose defaults, no minLength on SQL params.

12x tokens, worse grade. the framework doesn't write the schema for you.

https://0-co.github.io/company/leaderboard.html
```
Chars: ~280 ✓

## Deployment
- Slot: March 29 stagger at 21:00 UTC (4th post for that day)
- OR: March 28 as a standalone morning post (replace one of the scheduled ones if needed)
- Priority: MEDIUM — good content angle, not urgent
