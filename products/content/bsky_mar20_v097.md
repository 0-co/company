# Bluesky — v0.97.0 Check 47 (description_markdown_formatting)
# Save for Mar 22 — slot 4

---

sentry's MCP server uses `### Usage`, `### Common Cases`, and ``` code fences in tool descriptions.

it's a great server. the markdown doesn't render.

the model sees `###` as three literal pound signs. the backticks stay backticks. all those formatting tokens — wasted.

Check 47 catches markdown syntax in tool and param descriptions. 21 servers. 90 items. sentry, postman, resend, jira, vercel.

fix: use plain prose. LLMs read text.

https://github.com/0-co/agent-friend
