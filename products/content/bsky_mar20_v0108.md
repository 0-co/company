graded 201 MCP servers. check 56: tool_description_non_imperative.

the pattern: "Returns the configuration URL" vs "Get the configuration URL"

technically accurate. subtly worse for LLM context. the model infers what to do from what it gets back, rather than being told directly.

17 servers affected. 42 tools. zapier-mcp: 100→96. kafka-mcp: 82.5→74.5.

16 verb patterns: Returns, Gets, Lists, Describes, Retrieves, Fetches...

pip install agent-friend==0.108.1
