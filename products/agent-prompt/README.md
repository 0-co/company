# agent-prompt

Prompt templates for AI agents. LangChain has prompt templates. You don't need LangChain.

```python
from agent_prompt import PromptTemplate, ChatTemplate

tmpl = PromptTemplate("You are a {role}. Answer: {question}")
msg  = tmpl.to_message("system", role="Python expert", question="What is a decorator?")
# {"role": "system", "content": "You are a Python expert. Answer: What is a decorator?"}
```

Zero dependencies. `{variable}` syntax. Token estimation. Version pinning. Works with Anthropic and OpenAI.

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-prompt
```

## When you need this

Every AI agent has prompts scattered in Python strings, f-strings, and random `{}.format()` calls. You can't version them, test them, or estimate their cost before sending. LangChain's `PromptTemplate` works but pulls in the entire framework as a dependency.

`agent-prompt` gives you prompt templating, multi-turn chat templates, token estimation, and version tracking — in one zero-dep library.

## PromptTemplate

Simple `{variable}` placeholder syntax. Escape literal braces with doubling: `{{` → `{`.

```python
from agent_prompt import PromptTemplate

tmpl = PromptTemplate("You are a {role}. Respond to: {query}")

# Render to string
text = tmpl.render(role="Python expert", query="Explain decorators")

# Render as message dict (Anthropic/OpenAI compatible)
msg = tmpl.to_message("system", role="Python expert", query="Explain decorators")
# {"role": "system", "content": "You are a Python expert. Respond to: Explain decorators"}

# What variables does this template need?
tmpl.variables  # ["query", "role"]

# Estimate tokens before the API call
tmpl.estimate_tokens(role="Python expert", query="Explain decorators")  # ~12

# Escape literal braces
code_tmpl = PromptTemplate("Use {{braces}} in Python. Now explain: {concept}")
code_tmpl.render(concept="f-strings")
# "Use {braces} in Python. Now explain: f-strings"
```

## Partial templates

Pre-fill some variables, leave others for later:

```python
base = PromptTemplate("You are a {role}. Context: {context}. Answer: {question}")
support_bot = base.partial(role="customer support agent")

# Now only needs context and question
msg = support_bot.render(context="Order #1234", question="Where is my package?")
```

## ChatTemplate

Multi-turn conversation templates with shared variables:

```python
from agent_prompt import ChatTemplate, PromptTemplate

chat = ChatTemplate(
    system=PromptTemplate("You are a {expertise} expert. Be {style}."),
    turns=[
        ("user",      PromptTemplate("Explain {topic} briefly.")),
        ("assistant", PromptTemplate("Of course. {topic} is...")),
        ("user",      PromptTemplate("Give me an example.")),
    ],
)

messages = chat.render(expertise="Python", style="concise", topic="decorators")
# [
#   {"role": "system",    "content": "You are a Python expert. Be concise."},
#   {"role": "user",      "content": "Explain decorators briefly."},
#   {"role": "assistant", "content": "Of course. decorators is..."},
#   {"role": "user",      "content": "Give me an example."},
# ]

# Use directly with Anthropic
response = client.messages.create(
    model="claude-sonnet-4-6",
    system=messages[0]["content"],
    messages=messages[1:],
    max_tokens=500,
)

# Estimate total tokens before sending
chat.estimate_tokens(expertise="Python", style="concise", topic="decorators")  # ~30
```

Build the chat incrementally:

```python
chat = ChatTemplate(system=PromptTemplate("You are {role}."))
chat.add_turn("user", PromptTemplate("Hello!"))
chat.add_turn("assistant", PromptTemplate("Hi there!"))
chat.add_turn("user", PromptTemplate("Tell me about {topic}."))

msgs = chat.render(role="assistant", topic="Python")
```

## PromptVersion

Track and pin prompt versions by content hash:

```python
from agent_prompt import PromptVersion, PromptTemplate

tmpl = PromptTemplate("You are a {role}. Answer: {question}")
v1 = PromptVersion(tmpl, label="v1.0", metadata={"author": "eng"})

print(v1.hash)      # "a3f8c2d91e4b" — SHA-256 prefix of template content
print(v1.label)     # "v1.0"

# Use as normal template
msg = v1.to_message("system", role="expert", question="What is entropy?")

# Compare versions — equality is hash-based
v1b = PromptVersion(PromptTemplate("You are a {role}. Answer: {question}"))
v2  = PromptVersion(PromptTemplate("You are an expert {role}. Answer: {question}"))

v1 == v1b  # True — same content
v1 == v2   # False — different content

# A/B testing
active_prompt = v1 if experiment_condition else v2
result = active_prompt.render(role="assistant", question="Hello?")
```

## Token estimation

Rough but useful: ~4 chars per token, ±20%. Good for pre-flight checks and prompt budgeting.

```python
from agent_prompt import estimate_tokens
from agent_prompt.estimate import estimate_messages_tokens

estimate_tokens("You are a helpful assistant.")   # ~7

msgs = [
    {"role": "system", "content": "You are helpful."},
    {"role": "user",   "content": "What is Python?"},
]
estimate_messages_tokens(msgs)   # ~15 (includes per-message overhead)
```

For exact counts: use `client.count_tokens()` (Anthropic) or `tiktoken` (OpenAI).

## Message helper

```python
from agent_prompt import Message, PromptTemplate

msg = Message.from_template("user", PromptTemplate("Hello, {name}!"), name="Alice")
msg.to_dict()         # {"role": "user", "content": "Hello, Alice!"}
msg.estimate_tokens() # ~5
```

## Tests

```bash
python3 -m unittest tests.test_prompt -v
# 68 tests in ~0.01s
```

---

Built by [0co](https://0-co.github.io/company/) — an AI-operated company, live on Twitch.
