"""Example MCP server with real security vulnerabilities — for testing mcp-patch."""

import os
import subprocess
import pathlib
import requests
import httpx
import urllib.request

try:
    from mcp import tool
except ImportError:
    # Stub for testing without mcp installed
    def tool(fn):
        return fn


# --- shell_injection ---

@tool
def run_command(cmd: str) -> str:
    """Run a shell command (VULNERABLE: shell injection)."""
    result = subprocess.run(f"echo {cmd}", shell=True, capture_output=True, text=True)
    return result.stdout


@tool
def list_directory(path: str) -> str:
    """List a directory (VULNERABLE: shell injection via os.system)."""
    os.system(f"ls -la {path}")
    return "done"


@tool
def search_files(pattern: str) -> str:
    """Search for files (VULNERABLE: shell injection via os.popen)."""
    return os.popen(f"find / -name {pattern}").read()


@tool
def compile_code(source: str) -> str:
    """Compile code (VULNERABLE: shell injection with format)."""
    subprocess.Popen("gcc {}".format(source), shell=True)
    return "compiling"


# --- path_traversal ---

@tool
def read_file(filename: str) -> str:
    """Read a file (VULNERABLE: path traversal)."""
    with open(filename, "r") as f:
        return f.read()


@tool
def write_config(config_path: str, content: str) -> str:
    """Write config (VULNERABLE: path traversal on config_path)."""
    with open(config_path, "w") as f:
        f.write(content)
    return "written"


@tool
def load_template(template: str) -> str:
    """Load a template (VULNERABLE: path traversal via pathlib.Path)."""
    return pathlib.Path(template).read_text()


# --- ssrf ---

@tool
def fetch_url(url: str) -> str:
    """Fetch a URL (VULNERABLE: SSRF)."""
    return requests.get(url).text


@tool
def post_webhook(webhook_url: str, payload: str) -> str:
    """Post to webhook (VULNERABLE: SSRF)."""
    requests.post(webhook_url, data=payload)
    return "sent"


@tool
def proxy_request(endpoint: str) -> str:
    """Proxy a request (VULNERABLE: SSRF via httpx)."""
    return httpx.get(endpoint).text


@tool
def fetch_resource(resource_url: str) -> bytes:
    """Fetch a resource (VULNERABLE: SSRF via urllib)."""
    with urllib.request.urlopen(resource_url) as response:
        return response.read()


# --- helper function, not a tool (should NOT be flagged) ---

def _internal_fetch(url: str) -> str:
    """Not a @tool — should not be flagged even with requests.get(url)."""
    return requests.get(url).text


def _run_safely(cmd: str) -> str:
    """Not a @tool — should not be flagged."""
    return subprocess.run(cmd, shell=True).stdout
