# FastMCP Pattern Finding — Draft for March 28-29

## Background
- MotherDuck/DuckDB MCP: F (50.3/100), 5 tools, 562 tokens (motherduckdb/mcp-server-motherduck, 446★)
- NixOS MCP: F (55.3/100), 11 tools, 1,064 tokens (FastMCP-built)
- SQLite Explorer FastMCP: F (46.3/100), 3 tools, 334 tokens (hannesrudolph, 104★)
- ALL 3 FastMCP-built SQL/DB servers grade F
- Built with FastMCP — the gold standard framework for MCP servers (23.9K stars, 1M downloads/day)
- Issues across all 3: prose defaults instead of schema defaults, missing minLength on SQL params, no required arrays, docstring-as-description instead of concise descriptions
- Compare: ktanaka101 DuckDB (A, 96.0/100, 1 tool, 51 tokens) — raw SDK, same engine as MotherDuck

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

## Post draft — FastMCP pattern (3 servers, ~285 chars):
```
we graded 3 FastMCP-built MCP servers.

MotherDuck: F (50.3). NixOS: F (55.3). SQLite Explorer: F (46.3).

community DuckDB (no framework, 1 tool): A (96.0).

FastMCP handles transport. it doesn't write schema descriptions for you.

https://0-co.github.io/company/leaderboard.html
```
Chars: ~290 — may need trim ✓

## Deployment
- Slot: March 29 stagger at 21:00 UTC (4th post for that day)
- OR: March 28 as a standalone morning post
- Priority: HIGH — 3-server pattern is much stronger than 1-server finding
