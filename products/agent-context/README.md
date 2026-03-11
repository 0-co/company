# agent-context

Long conversations make LLMs worse. Not a theory — it shows up in benchmarks, evals, and production logs. Models tested across ~18 architectures all show coherence degradation after roughly 30 turns. The model starts contradicting itself, forgetting constraints, repeating earlier answers. The context window is full; the useful signal is buried.

The fix is not complicated: stop sending the whole history. agent-context does that for you.

---

## When you need this

- **Long-running agents** — chatbots, coding assistants, or tool-calling loops that accumulate messages over many turns
- **Multi-turn conversations** — agent starts contradicting itself or forgetting earlier instructions around turn 30+
- **Token cost control** — sending the full history on every call multiplies token costs linearly; truncation cuts that
- **Context window errors** — hitting `context_length_exceeded` (400) in production because a conversation grew too long
- **Production API servers** — manage context per-session, call `ctx.clear()` when a session ends
- **Works with any LLM** — Anthropic, OpenAI, or any client that takes a `messages` list

---

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-context
```

No dependencies. Python 3.9+.

---

## Quick start

```python
from agent_context import ContextManager

ctx = ContextManager(max_turns=20, system="You are a helpful assistant.")

# Add messages as the conversation progresses.
ctx.add("user", "What is the capital of France?")
ctx.add("assistant", "Paris.")
ctx.add("user", "What river runs through it?")
ctx.add("assistant", "The Seine.")

# Pass directly to your LLM client.
messages = ctx.get()
response = client.messages.create(model="...", messages=messages, ...)

ctx.add("assistant", response.content[0].text)
```

`ctx.get()` returns only the messages that fit the window. Your LLM call never sees the full history — just the relevant tail.

---

## Three strategies

### 1. Sliding window

Keep the last N messages. Simple, predictable, zero cost.

```python
ctx = ContextManager(max_turns=20)
```

Old messages are dropped as new ones arrive. If you set `max_turns=20`, the model always sees the 20 most recent messages, no matter how long the conversation runs.

### 2. Token budget

Keep the newest messages that fit within a token budget. Better than turn count when message length varies.

```python
ctx = ContextManager(max_tokens=4000)
```

Token estimation uses `len(text) // 4` — a rough heuristic, but accurate enough for pruning decisions and requires no external tokenizer.

### 3. Compress

Keep the first N turns, compress the middle via a summarizer, keep the last N turns.

```python
def summarize(messages: list[dict]) -> str:
    # Call your LLM here, or use a simple heuristic.
    return f"[{len(messages)} messages summarized]"

ctx = ContextManager(
    max_turns=20,
    strategy="compress",
    summarizer=summarize,
    keep_first=2,
    keep_last=4,
)
```

The summary is inserted as an assistant message so it reads naturally in context. Without a summarizer, falls back to sliding window.

---

## API reference

### `ContextManager`

```python
ctx = ContextManager(
    max_turns=20,           # keep last N messages (default: 20)
    max_tokens=4000,        # keep newest messages within token budget
    strategy="sliding_window",  # "sliding_window" | "token_budget" | "compress"
    summarizer=fn,          # fn(messages: list[dict]) -> str (compress only)
    keep_first=2,           # messages to keep at start (compress only)
    keep_last=4,            # messages to keep at end (compress only)
    system="...",           # system prompt — always prepended, never trimmed
    raise_on_overflow=False # raise ContextOverflow instead of silently pruning
)
```

Strategy defaults:
- `max_tokens` set → `token_budget`
- `max_turns` set → `sliding_window`
- Neither set → `sliding_window` with `max_turns=20`

#### Methods

**`add(role, content)`** — Append a message to history.

**`get()`** — Return trimmed message list, ready to pass to an LLM client. System message prepended if set.

**`clear()`** / **`reset()`** — Clear all history. System prompt retained.

#### Properties

| Property | Type | Description |
|---|---|---|
| `total_turns` | int | Total messages added over the lifetime |
| `current_turns` | int | Messages in the current window |
| `tokens_estimate` | int | Rough token count of the current window |

---

### `trim()`

Stateless functional interface. Takes a message list, returns a trimmed list.

```python
from agent_context import trim

short = trim(messages, max_turns=10)
short = trim(messages, max_tokens=4000)
short = trim(messages, max_tokens=4000, strategy="compress", summarizer=fn)
short = trim(messages, max_turns=10, system="You are helpful.")
```

Useful when you don't need stateful tracking — just a one-shot reduction.

---

### `ContextOverflow`

Raised when `raise_on_overflow=True` and the context exceeds its limit.

```python
from agent_context import ContextOverflow

ctx = ContextManager(max_turns=10, raise_on_overflow=True)

try:
    ctx.add("user", "...")
except ContextOverflow as e:
    print(e.limit_type)   # "turns" or "tokens"
    print(e.limit)        # configured limit
    print(e.current)      # value at time of violation
    print(e.msg)          # human-readable (also str(e))
```

---

## How it works

**Token estimation**: `len(text) // 4`. No tokenizer needed. Real token counts vary by model (GPT-4 tokenizes differently from Claude), but the heuristic is close enough for pruning — you're making a best-effort size estimate, not accounting.

**Sliding window**: `messages[-max_turns:]`. Nothing clever. The system message is always re-prepended after the slice.

**Token budget**: Walks the message list from newest to oldest, accumulating token estimates until the budget is exhausted. The system message is not counted against the budget — it always fits.

**Compress**: Splits the history into three blocks — `messages[:keep_first]`, the middle, and `messages[-keep_last:]`. The middle is passed to your summarizer. The result is re-joined as `[first] + [summary message] + [last]`. Without a summarizer, falls back to sliding window.

**System message**: Stored separately. Never counted against limits. Always prepended by `get()`. Messages added with `role="system"` via `add()` are treated as regular messages — use the `system=` parameter for persistent system prompts.

---

## Example: Anthropic agent loop

```python
import anthropic
from agent_context import ContextManager

client = anthropic.Anthropic()

ctx = ContextManager(
    max_turns=10,
    system="You are a concise assistant.",
)

questions = ["What is Paris?", "Name a monument there.", "How tall is it?"]

for question in questions:
    ctx.add("user", question)

    messages = ctx.get()
    # Strip system message — Anthropic takes it separately.
    system_msg = next((m["content"] for m in messages if m["role"] == "system"), None)
    chat_msgs = [m for m in messages if m["role"] != "system"]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        system=system_msg or "",
        messages=chat_msgs,
    )
    answer = response.content[0].text
    ctx.add("assistant", answer)

    print(f"Q: {question}")
    print(f"A: {answer}")
    print(f"Window: {ctx.current_turns} msgs, ~{ctx.tokens_estimate} tokens\n")
```

---

## Why not just increase the context window?

You can. Models now support 128K-200K token contexts. But:

1. Latency scales with context length. A 100K token prompt is slower and more expensive than a 4K one.
2. "Lost in the middle" is documented: models attend less to content buried in the middle of long contexts.
3. For most agent tasks, the last 10-20 turns contain all the relevant state. The rest is noise.

Pruning is not a workaround for small context windows. It's what you do when you want quality and cost predictability regardless of conversation length.

---

Built at [0co](https://github.com/0-co/company) — an AI autonomously running a startup.
