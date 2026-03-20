sendgrid is an email company.

their MCP server has a param named `email`.

no `format: "email"`.

the model has to guess it's an email address — not a name, not a username, not "john@". just a vibe.

stripe, klaviyo, shopify, doppler: same problem.

59 servers. 244 string params that look like emails/URLs/dates but don't say so.

v0.86.0 of agent-friend now flags this.

pip install agent-friend
