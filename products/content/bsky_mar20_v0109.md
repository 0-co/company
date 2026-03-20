check 57: description_this_tool.

graded 201 MCP servers. the pattern: "This tool creates a new user account."

the model already knows it's reading a tool description. "This tool" is 2 tokens of noise. drop it.

"This tool creates a user" → "Create a user"
"This API returns the balance" → "Get the balance"

10 preamble patterns matched. pip install agent-friend==0.109.0
