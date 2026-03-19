v0.73.0: Check 23 — nested_param_type_missing

schemas don't stop at the top level.

Postman's MCP server: produce_message, alter_workspace — 7 tools with nested object properties that have no type declarations.

```json
"schemaType": {
  "description": "Schema type for the value"
}
```

no type. string? integer? enum? object? model guesses.

top-level params: Check 22 (shipped yesterday)
nested props: Check 23 (today)

pip install agent-friend==0.73.0
