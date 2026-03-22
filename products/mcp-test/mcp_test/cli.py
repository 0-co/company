"""CLI entrypoint for mcp-test."""

import argparse
import json
import sys
from mcp_test.client import MCPClient, MCPError


def cmd_list(args):
    """List all tools exposed by the server."""
    with MCPClient(args.server.split(), timeout=args.timeout) as client:
        tools = client.list_tools()
        if not tools:
            print("No tools found.")
            return
        print(f"Found {len(tools)} tools:\n")
        for t in tools:
            print(f"  {t['name']}")
            if t.get("description"):
                desc = t["description"][:80].replace("\n", " ")
                print(f"    {desc}")
            schema = t.get("inputSchema", {})
            props = schema.get("properties", {})
            required = schema.get("required", [])
            if props:
                params = []
                for name, prop in props.items():
                    req = "*" if name in required else ""
                    params.append(f"{name}{req}:{prop.get('type','?')}")
                print(f"    params: {', '.join(params)}")
            print()


def cmd_call(args):
    """Call a specific tool with JSON arguments."""
    try:
        arguments = json.loads(args.args) if args.args else {}
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON arguments: {e}", file=sys.stderr)
        sys.exit(1)

    with MCPClient(args.server.split(), timeout=args.timeout) as client:
        try:
            result = client.call(args.tool, arguments)
            if isinstance(result, str):
                print(result)
            else:
                print(json.dumps(result, indent=2))
        except MCPError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def cmd_check(args):
    """Smoke-test a server: verify it starts, lists tools, and each tool responds."""
    print(f"Connecting to: {args.server}")
    errors = 0
    try:
        with MCPClient(args.server.split(), timeout=args.timeout) as client:
            tools = client.list_tools()
            print(f"✓ Server started, {len(tools)} tools listed")

            if args.smoke:
                print("\nSmoke testing tools (no arguments)...")
                for tool in tools:
                    name = tool["name"]
                    schema = tool.get("inputSchema", {})
                    required = schema.get("required", [])
                    if required:
                        print(f"  skip {name} (has required params: {', '.join(required)})")
                        continue
                    try:
                        client.call_raw(name, {})
                        print(f"  ✓ {name}")
                    except MCPError as e:
                        print(f"  ✗ {name}: {e}")
                        errors += 1

    except MCPError as e:
        print(f"✗ Failed to connect: {e}", file=sys.stderr)
        sys.exit(1)

    if errors:
        print(f"\n{errors} tool(s) failed smoke test")
        sys.exit(1)
    else:
        print("\nAll checks passed.")


def main():
    parser = argparse.ArgumentParser(
        prog="mcp-test",
        description="Test MCP servers from the command line",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="Call timeout in seconds")

    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="List tools exposed by the server")
    p_list.add_argument("server", help="Command to start the server (e.g. 'python server.py')")

    # call
    p_call = sub.add_parser("call", help="Call a specific tool")
    p_call.add_argument("server", help="Command to start the server")
    p_call.add_argument("tool", help="Tool name to call")
    p_call.add_argument("args", nargs="?", default=None, help="JSON arguments (e.g. '{\"query\":\"test\"}')")

    # check
    p_check = sub.add_parser("check", help="Smoke-test a server")
    p_check.add_argument("server", help="Command to start the server")
    p_check.add_argument("--smoke", action="store_true", help="Also call each tool with no arguments")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {"list": cmd_list, "call": cmd_call, "check": cmd_check}
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
