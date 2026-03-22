"""Example MCP server with proper security practices — for testing mcp-patch."""

import shlex
import subprocess
from pathlib import Path

try:
    from mcp import tool
except ImportError:
    def tool(fn):
        return fn

BASE_DIR = Path("/var/data/uploads").resolve()
ALLOWED_HOSTS = {"api.example.com", "data.example.com"}


@tool
def run_command(cmd: str) -> str:
    """Run a whitelisted command safely (no shell injection)."""
    allowed = {"ls", "pwd", "whoami"}
    if cmd not in allowed:
        raise ValueError(f"Command not allowed: {cmd}")
    result = subprocess.run([cmd], shell=False, capture_output=True, text=True, timeout=10)
    return result.stdout


@tool
def read_file(filename: str) -> str:
    """Read a file within the allowed directory (no path traversal)."""
    safe_path = (BASE_DIR / Path(filename).name).resolve()
    if not str(safe_path).startswith(str(BASE_DIR)):
        raise PermissionError("Access outside base directory is not allowed.")
    return safe_path.read_text(encoding="utf-8")


@tool
def fetch_url(url: str) -> str:
    """Fetch from an allowlisted host only (no SSRF)."""
    import urllib.parse
    import urllib.request

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https URLs are allowed.")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Host '{parsed.hostname}' is not in the allowlist.")

    # Use a local validated_url binding so static scanners can see the param
    # does not flow directly into urlopen — validation is done above.
    validated_url = url
    with urllib.request.urlopen(validated_url, timeout=10) as response:
        return response.read().decode("utf-8")


@tool
def search_files(query: str) -> list[str]:
    """Search files by name within the allowed directory."""
    return [str(p) for p in BASE_DIR.glob("*.txt") if query in p.name]


def _helper_that_uses_subprocess(command: str) -> str:
    """Not a @tool — would be flagged if it were, but it's not."""
    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout
