"""Minimal MCP server for testing mcp-test itself."""

import json
import sys


def handle_initialize(msg_id, params):
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "example-server", "version": "0.1.0"},
        },
    }


def handle_tools_list(msg_id):
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "tools": [
                {
                    "name": "echo",
                    "description": "Return the input message unchanged.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string", "description": "Message to echo"}
                        },
                        "required": ["message"],
                    },
                },
                {
                    "name": "add",
                    "description": "Add two integers.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "integer"},
                            "b": {"type": "integer"},
                        },
                        "required": ["a", "b"],
                    },
                },
            ]
        },
    }


def handle_tools_call(msg_id, params):
    name = params.get("name")
    args = params.get("arguments", {})

    if name == "echo":
        msg = args.get("message", "")
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [{"type": "text", "text": msg}],
                "isError": False,
            },
        }
    elif name == "add":
        result = args.get("a", 0) + args.get("b", 0)
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [{"type": "text", "text": str(result)}],
                "isError": False,
            },
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Unknown tool: {name}"},
        }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = msg.get("method")
        msg_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            response = handle_initialize(msg_id, params)
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            response = handle_tools_list(msg_id)
        elif method == "tools/call":
            response = handle_tools_call(msg_id, params)
        else:
            if msg_id is None:
                continue
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
