# mcp-patch

Static security scanner for Python MCP server code.

43% of popular MCP servers have shell injection vulnerabilities. No existing tool does AST-level scanning with MCP context awareness. This one does.

## Real CVEs this would have caught

- **CVE-2025-53967** (Framelink Figma MCP) — shell injection via unsanitized tool parameters
- **CVE-2025-6514** (mcp-remote, 437K downloads) — arbitrary command execution via unsanitized tool params

## Install

```
pip install mcp-patch
mcp-patch scan my_server.py
```

## Usage

```
# Scan a single file
mcp-patch scan server.py

# Scan a directory
mcp-patch scan ./servers/
```

## Example output

```
Scanning server.py...

  CRITICAL  shell_injection  line 14
  subprocess.run(f"ls {path}", shell=True)
  subprocess.run(shell=True) — tool param 'path' flows to shell
  Fix: Use subprocess.run([cmd, shlex.quote(arg)]) without shell=True

  HIGH      path_traversal   line 28
  open(filename)
  open(filename) — tool param 'filename' used as file path without validation
  Fix: Use (base_dir / Path(filename).name).resolve() and verify result starts with base_dir

Found 2 issues (1 CRITICAL, 1 HIGH) in 1 file.
```

## Checks

| Check | Severity | What it detects |
|---|---|---|
| `shell_injection` | CRITICAL | `subprocess.run/Popen/call(f"...{param}", shell=True)`, `os.system()`, `os.popen()` with tool params |
| `path_traversal` | HIGH | `open(param)`, `Path(param)` with a tool param passed directly as a path |
| `ssrf` | HIGH | `requests.get/post(url)`, `httpx.get(url)`, `urllib.request.urlopen(url)` where `url` is a tool param |

Only functions decorated with `@tool` or `@mcp.tool()` are scanned. Plain helper functions are ignored.

## How it works

Pure stdlib. No network calls. No LLM. Parses your Python source with the `ast` module, finds `@tool` decorated functions, collects their parameter names, then walks each function body looking for dangerous call patterns where user-controlled params flow into dangerous sinks.

## False positives

This is an MVP scanner — it prefers to over-report rather than miss real vulnerabilities. A `path_traversal` finding on `open(filename)` is real even if you have runtime validation elsewhere; the fix is to move validation into the same function so the scanner (and reviewers) can see it.

## Development

```
python -m pytest tests/
```

No external dependencies. Python 3.9+.
