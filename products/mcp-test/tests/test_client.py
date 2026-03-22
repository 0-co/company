"""Tests for mcp_test.client using the example server."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from mcp_test.client import MCPClient, MCPError

SERVER_CMD = [sys.executable, os.path.join(os.path.dirname(__file__), "example_server.py")]


@pytest.fixture(scope="module")
def server():
    with MCPClient(SERVER_CMD) as s:
        yield s


class TestListTools:
    def test_list_returns_tools(self, server):
        tools = server.list_tools()
        assert len(tools) == 2

    def test_tool_names(self, server):
        names = server.tool_names()
        assert "echo" in names
        assert "add" in names

    def test_tools_have_schema(self, server):
        tools = server.list_tools()
        for t in tools:
            assert "name" in t
            assert "inputSchema" in t


class TestCallTools:
    def test_echo_returns_message(self, server):
        result = server.call("echo", {"message": "hello world"})
        assert result == "hello world"

    def test_echo_empty_string(self, server):
        result = server.call("echo", {"message": ""})
        assert result == ""

    def test_add_integers(self, server):
        result = server.call("add", {"a": 3, "b": 4})
        assert result == "7"

    def test_add_negative(self, server):
        result = server.call("add", {"a": -5, "b": 3})
        assert result == "-2"

    def test_unknown_tool_raises(self, server):
        with pytest.raises(MCPError):
            server.call("nonexistent_tool", {})

    def test_call_raw_returns_dict(self, server):
        result = server.call_raw("echo", {"message": "test"})
        assert "content" in result
        assert result["isError"] is False
