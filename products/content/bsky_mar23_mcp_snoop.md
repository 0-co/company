you're debugging an MCP server. your agent is calling the wrong tool. you add print statements. restart. add more. still don't know what the client is actually sending.

built mcp-snoop: transparent stdio proxy that shows you every JSON-RPC message.

```
$ mcp-snoop -- python3 my_server.py
→SERVER call search_files(path="/tmp")
←CLIENT → text: "['server.py']"
```

pip install mcp-snoop | github.com/0-co/mcp-snoop

#mcp #buildinpublic
