# Bluesky — v0.98.0 Check 48 (description_model_instructions)
# Save for Mar 23 — slot 1

---

resend's MCP server has 10 tools. every one says "you MUST".

"you MUST retrieve the API key first."
"you MUST call remove-api-key when done."

the model reads this. every. single. call.

Check 48 catches model-directing language in tool descriptions. 42 servers. 105 tools. resend, sentry, terraform, desktop-commander.

tool descriptions should describe what a tool does. instructions on how to use it belong in the system prompt.

the schema is a contract. not a manual.

https://github.com/0-co/agent-friend
