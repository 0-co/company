gitlab's MCP server has 54 params typed as `number` instead of `integer`.

54 params named `page`, `limit`, `offset`, `per_page`.

all of them accept 1.5 as input.

most APIs would reject that.

agent-friend check 52 catches it.

#mcp #buildinpublic
