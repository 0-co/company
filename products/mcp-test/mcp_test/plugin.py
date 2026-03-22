"""pytest plugin — provides the mcp_server fixture."""

import pytest
from mcp_test.client import MCPClient


def pytest_addoption(parser):
    parser.addoption(
        "--mcp-server",
        action="store",
        default=None,
        help="Command to start the MCP server under test (e.g. 'python server.py')",
    )
    parser.addoption(
        "--mcp-timeout",
        action="store",
        type=float,
        default=30.0,
        help="Timeout in seconds for MCP calls (default: 30)",
    )


@pytest.fixture(scope="session")
def mcp_server(request):
    """Session-scoped fixture that provides a connected MCPClient.

    Configure via --mcp-server CLI option or mcp_server_command in pytest.ini:

        [pytest]
        mcp_server_command = python my_server.py

    Example test::

        def test_tools_exist(mcp_server):
            tools = mcp_server.list_tools()
            assert len(tools) > 0

        def test_search(mcp_server):
            result = mcp_server.call("search", {"query": "test"})
            assert isinstance(result, str)
            assert len(result) > 0
    """
    command = request.config.getoption("--mcp-server")
    if not command:
        command = request.config.getini("mcp_server_command")
    if not command:
        pytest.skip("No MCP server command specified. Use --mcp-server or mcp_server_command in pytest.ini")

    timeout = request.config.getoption("--mcp-timeout")
    client = MCPClient(command.split() if isinstance(command, str) else command, timeout=timeout)
    yield client
    client.close()


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "mcp: mark test as an MCP server integration test",
    )
