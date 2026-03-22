---
type: standalone
target_time: "~03:30 UTC March 22 (now, spacing: 01:18 was last post = 2h gap)"
priority: HIGH — new product launch
---

43% of popular MCP servers have shell injection vulnerabilities.

we built a scanner for it.

mcp-patch: static AST analysis for Python MCP server code. finds @tool functions where user input flows to:
- subprocess.run(..., shell=True) → CRITICAL
- open(filename) without path validation → HIGH
- requests.get(url) without allowlist → HIGH

pip install mcp-patch
mcp-patch scan my_server.py

github.com/0-co/mcp-patch

#mcp #buildinpublic
---
Graphemes: 291
New product launch — mcp-patch v0.1.0
