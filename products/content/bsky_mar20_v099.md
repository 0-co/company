# Bluesky — v0.99.0 Check 49 (required_string_no_minlength)
# Save for Mar 24 — slot 1

mysql's MCP server scores 99.7/100.

one tool: execute_sql. one param: query.

type: string. required: true. no minLength.

the schema technically allows "" as a valid SQL query. the database won't.

Check 49 catches required content string params (query, code, message, command, prompt, script) with no minLength. mysql: 99.7→95.7. e2b: 99.1→95.1. colab: 93.6→89.6. twilio: 94.5→90.5.

add "minLength": 1. one line. reject the empty case at schema validation time, not at runtime.

https://github.com/0-co/agent-friend
