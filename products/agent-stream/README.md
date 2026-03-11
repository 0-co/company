# agent-stream

Streaming LLM response handling for AI agents. Collect chunks, track tokens, handle cancellation.

```python
from agent_stream import StreamCollector

collector = StreamCollector(on_chunk=lambda t: print(t, end="", flush=True))
result = collector.stream_anthropic(client, model="claude-sonnet-4-6", max_tokens=500,
                                    messages=[{"role": "user", "content": "Hello"}])
print()
print(f"Tokens: {result.total_tokens}, took {result.duration_ms:.0f}ms")
```

Zero dependencies. Normalizes Anthropic and OpenAI streaming formats. Sync and async.

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-stream
```

## When you need this

The Anthropic and OpenAI streaming APIs are different. Anthropic sends `content_block_delta` events; OpenAI sends `choices[0].delta.content`. Token usage arrives at different points. Error handling is different. And both change between SDK versions.

`agent-stream` normalizes both into a `StreamResult` with `text`, `input_tokens`, `output_tokens`, `duration_ms`, and `stop_reason`. Add an `on_chunk` callback for real-time display, a `cancel_event` for mid-stream cancellation, and you have a complete streaming layer.

## StreamResult

```python
result.text           # "The answer is 42"
result.input_tokens   # 25
result.output_tokens  # 8
result.total_tokens   # 33
result.stop_reason    # "end_turn" / "max_tokens" / "stop" / "cancelled"
result.duration_ms    # 847.3
result.model          # "claude-sonnet-4-6"
result.chunks         # ["The", " answer", " is", " 42"]
result.was_cancelled  # False
```

## StreamCollector (synchronous)

```python
from agent_stream import StreamCollector

# Basic usage — collect and return
collector = StreamCollector()
result = collector.stream_anthropic(client,
    model="claude-sonnet-4-6",
    max_tokens=500,
    messages=[{"role": "user", "content": "Explain recursion"}],
)

# Real-time display with on_chunk callback
collector = StreamCollector(on_chunk=lambda t: print(t, end="", flush=True))
result = collector.stream_anthropic(client, model="claude-sonnet-4-6", ...)
print()  # newline after stream

# Cancellation
import threading
cancel = threading.Event()

def call_api():
    return collector.stream_anthropic(client, ...)

# In another thread: cancel.set() to stop mid-stream
```

**OpenAI:**
```python
result = collector.stream_openai(client,
    model="gpt-4o",
    max_tokens=500,
    messages=[{"role": "user", "content": "Hello"}],
)
# Note: stream=True is added automatically
```

**Collect from an existing stream object:**
```python
with client.messages.stream(model=..., max_tokens=..., messages=...) as stream:
    result = collector.collect_anthropic(stream)
```

## AsyncStreamCollector

```python
from agent_stream import AsyncStreamCollector
import asyncio

async def main():
    collector = AsyncStreamCollector(
        on_chunk=lambda t: print(t, end="", flush=True)
    )
    result = await collector.stream_anthropic(
        async_client,
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": "Hello"}],
    )
    print()
    return result

result = asyncio.run(main())

# Async on_chunk callback also works
async def on_chunk(text):
    await websocket.send_text(text)

collector = AsyncStreamCollector(on_chunk=on_chunk)
```

**Async cancellation with asyncio.Event:**
```python
import asyncio

cancel = asyncio.Event()
collector = AsyncStreamCollector(cancel_event=cancel)

async def main():
    task = asyncio.create_task(collector.stream_anthropic(client, ...))
    await asyncio.sleep(1)
    cancel.set()  # Stop after 1 second
    result = await task
    print(result.was_cancelled)  # True
```

## Error handling

All streaming errors are wrapped in `StreamError`:

```python
from agent_stream import StreamError

try:
    result = collector.stream_anthropic(client, ...)
except StreamError as e:
    print(f"Stream failed: {e}")
```

## Tests

```bash
python3 -m unittest tests.test_stream -v
# 43 tests in ~0.3s
```

---

Built by [0co](https://0-co.github.io/company/) — an AI-operated company, live on Twitch.
