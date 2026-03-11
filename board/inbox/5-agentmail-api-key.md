# AgentMail API Key for agent-friend v0.2

**Priority:** 3 (low urgency, enables a significant product enhancement)

## Why

agent-friend v0.1 ships today with web search, code execution, and memory. The obvious missing piece is email.

AgentMail launched this week (YC S25, $6M seed from General Catalyst, Paul Graham, Dharmesh Shah). They're the first API-first email provider built specifically for AI agents. Free tier: 3 inboxes, 3,000 emails/month, no credit card required.

This would enable:
```python
friend = Friend(
    tools=["search", "code", "memory", "email"],
    email_config={"api_key": "from_env"}
)
friend.chat("Draft a reply to my latest email from Alice")
```

An AI agent that can actually read and send email is a meaningfully different product than one that can't. It's also much better stream content — watching an agent manage email is more compelling than watching it search the web.

## Request

Sign up for AgentMail free tier at https://agentmail.to/ and add the API key to the vault as:
```
sudo -u vault /home/vault/bin/vault-agentmail
```

Or if simpler: just provide the `AGENTMAIL_API_KEY` env var and I'll add the email tool to agent-friend.

## API usage

```python
# The AgentMail Python SDK is already published on PyPI
# pip install agentmail

from agentmail import AgentMail
client = AgentMail(api_key=os.getenv("AGENTMAIL_API_KEY"))
inbox = client.inboxes.create(client_id="agent-friend-inbox")
messages = client.messages.list(inbox.id)
client.messages.send(inbox.id, to=["user@example.com"], subject="...", text="...")
```

This would make agent-friend the only personal agent library with working email out of the box.

## Alternative

If the board doesn't want to create an AgentMail account, I can implement email as an IMAP/SMTP tool instead (requires an email account's credentials), or skip email and focus on other integrations for v0.2.
