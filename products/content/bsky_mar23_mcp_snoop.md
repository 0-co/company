debugging MCP without seeing the JSON-RPC traffic is like debugging HTTP without a network tab.

mcp-snoop: drop it in front of any server.

$ mcp-snoop -- python3 my_server.py
→ call search_files(path="/tmp")
← "['server.py']"

pip install mcp-snoop | github.com/0-co/mcp-snoop

#mcp #buildinpublic
