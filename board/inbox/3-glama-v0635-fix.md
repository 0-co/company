# P3: Glama — v0.63.5 — Fix uv Build (mcp Python version marker)

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## What was wrong with v0.63.4

Glama runs `uv sync --extra all` during build. After v0.63.4, `pyproject.toml`'s `[all]` extras included `mcp>=1.0`. The `uv` resolver checked Python 3.9 compatibility (because `requires-python = ">=3.9"`) and failed because mcp requires Python 3.10+.

## The fix (v0.63.5)

Changed `pyproject.toml`:
```toml
# Before: empty deps + mcp in [all] extras
dependencies = []
# [all] = ["anthropic...", "openai...", "pyyaml...", "mcp>=1.0"]  ← FAILED on Python 3.9

# After: conditional dep with Python marker
dependencies = [
    "mcp>=1.0; python_version >= '3.10'"   ← skipped on Python 3.9, installed on Python 3.14
]
# [all] = ["anthropic...", "openai...", "pyyaml..."]  ← no mcp in extras anymore
```

## Why this works

On Python 3.14 (Glama's build environment):
- `python_version >= '3.10'` is True → mcp gets installed ✓

On Python 3.9 (old envs / CI):
- `python_version >= '3.10'` is False → mcp skipped ✓ (base library works without mcp)

## Commit

`55b0f47` on agent-friend main

## Action needed

1. Go to https://glama.ai/mcp/servers/0-co/agent-friend/admin/dockerfile
2. Deploy again — this is commit `55b0f47` (v0.63.5)
3. The `uv sync` step should now succeed (mcp installs on Python 3.14)
4. `python -m agent_friend` should start the MCP server

## Summary of the full chain

- v0.63.3: `__main__.py` calls `mcp_server:main()` (was `cli:main()`)
- v0.63.4: Dockerfile `mcp>=1.0` (was `>=1.25`, non-existent)
- v0.63.5: mcp as conditional dep with `python_version >= '3.10'` marker (fixes uv resolution)
