"""MCP client for testing — connects to a server via stdio."""

import json
import subprocess
import threading
import time
from typing import Any


class MCPError(Exception):
    """Raised when an MCP call fails or times out."""


class MCPClient:
    """Stdio client for testing MCP servers.

    Usage::

        server = MCPClient(["python", "my_server.py"])
        tools = server.list_tools()
        result = server.call("tool_name", {"arg": "value"})
        server.close()

    Or as a context manager::

        with MCPClient(["python", "my_server.py"]) as server:
            result = server.call("search", {"query": "hello"})
    """

    def __init__(self, command: list[str] | str, timeout: float = 30.0):
        """Start the MCP server process and initialize the session.

        Args:
            command: Command to start the server (list or shell string).
            timeout: Default timeout in seconds for each call.
        """
        if isinstance(command, str):
            command = command.split()
        self.command = command
        self.timeout = timeout
        self._msg_id = 0
        self._process: subprocess.Popen | None = None
        self._lock = threading.Lock()
        self._start()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def _start(self) -> None:
        self._process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        # Initialize the MCP session
        self._call_raw("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp-test", "version": "0.1.0"},
        })
        # Send initialized notification (no response expected)
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def close(self) -> None:
        """Terminate the server process."""
        if self._process and self._process.poll() is None:
            self._process.stdin.close()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    # ------------------------------------------------------------------
    # Low-level JSON-RPC
    # ------------------------------------------------------------------

    def _next_id(self) -> int:
        with self._lock:
            self._msg_id += 1
            return self._msg_id

    def _send(self, msg: dict) -> None:
        line = json.dumps(msg) + "\n"
        self._process.stdin.write(line)
        self._process.stdin.flush()

    def _recv(self, deadline: float) -> dict:
        """Read lines until we get a JSON-RPC response (has 'id')."""
        while True:
            if time.time() > deadline:
                raise MCPError(f"Timeout waiting for server response")
            # Non-blocking readline with poll
            import select
            ready, _, _ = select.select([self._process.stdout], [], [], 0.1)
            if not ready:
                if self._process.poll() is not None:
                    stderr = self._process.stderr.read()
                    raise MCPError(f"Server exited unexpectedly. Stderr: {stderr[:500]}")
                continue
            line = self._process.stdout.readline()
            if not line:
                raise MCPError("Server closed stdout")
            try:
                msg = json.loads(line)
                if "id" in msg:
                    return msg
                # Notification or log — skip
            except json.JSONDecodeError:
                pass  # Skip non-JSON lines (server log output etc.)

    def _call_raw(self, method: str, params: dict) -> dict:
        """Send a JSON-RPC request and return the raw response."""
        req_id = self._next_id()
        msg = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
        self._send(msg)
        deadline = time.time() + self.timeout
        response = self._recv(deadline)
        if "error" in response:
            raise MCPError(f"RPC error: {response['error']}")
        return response.get("result", {})

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_tools(self) -> list[dict]:
        """Return the list of tools the server exposes.

        Returns:
            List of tool dicts with 'name', 'description', 'inputSchema'.
        """
        result = self._call_raw("tools/list", {})
        return result.get("tools", [])

    def tool_names(self) -> list[str]:
        """Return just the tool names."""
        return [t["name"] for t in self.list_tools()]

    def call(self, tool_name: str, arguments: dict | None = None) -> Any:
        """Call a tool and return its content.

        Args:
            tool_name: The name of the tool to call.
            arguments: Dict of arguments to pass.

        Returns:
            The tool's result content (parsed from the MCP response).

        Raises:
            MCPError: If the tool call fails or returns an error.
        """
        result = self._call_raw("tools/call", {
            "name": tool_name,
            "arguments": arguments or {},
        })
        # MCP returns content as a list of content items
        content = result.get("content", [])
        if result.get("isError"):
            raise MCPError(f"Tool '{tool_name}' returned error: {content}")
        # Return text content if there's just one text item
        if len(content) == 1 and content[0].get("type") == "text":
            return content[0]["text"]
        return content

    def call_raw(self, tool_name: str, arguments: dict | None = None) -> dict:
        """Call a tool and return the raw MCP result dict (including isError)."""
        return self._call_raw("tools/call", {
            "name": tool_name,
            "arguments": arguments or {},
        })
