# agent-trace

Distributed tracing for multi-agent workflows. Zero dependencies.

When multiple AI agents call each other, failures are invisible. You get a timeout or a wrong answer and no idea which of the five hops caused it. agent-trace gives you trace IDs, parent-child span hierarchies, and timing data across process boundaries — so you can reconstruct exactly what happened.

---

## When you need this

**Coordinator/sub-agent architectures.** A planning agent spawns three workers. One returns garbage. You need to know which one, how long it took, and what it was doing when it failed.

**Tool call chains.** Agent calls search, then summarize, then write. You want timing per tool and a record of which calls succeeded before the one that didn't.

**Cross-process traces.** Agent A runs in one container, Agent B in another. You need the spans from both to appear in the same trace tree so you can read the full execution path.

**Debugging silent failures.** The agent returns a result but it's wrong. No exception was raised. You need event-level detail — what attributes were set, what events were logged at each step — to find the divergence.

---

## Installation

```
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-trace
```

No dependencies. Python 3.8+.

---

## Quick start

```python
from agent_trace import Tracer, trace_span, get_current_span

# Coordinator agent with two sub-agents
tracer = Tracer()

with tracer.start_span("coordinator") as coordinator_span:
    coordinator_span.set_attribute("model", "claude-sonnet-4-6")
    coordinator_span.set_attribute("input_tokens", 800)

    with tracer.start_span("sub_agent_1") as s1:
        s1.set_attribute("task", "fetch_documents")
        s1.add_event("tool_call", {"tool": "search", "query": "agent tracing"})
        # ... do work ...
        s1.set_attribute("output_tokens", 200)

    with tracer.start_span("sub_agent_2") as s2:
        s2.set_attribute("task", "summarize")
        try:
            # ... do work ...
            pass
        except Exception as exc:
            s2.record_error(exc)
            raise

    coordinator_span.set_attribute("output_tokens", 150)

# All spans collected
tree = tracer.get_trace_tree()
# {
#   "name": "coordinator",
#   "children": [
#     {"name": "sub_agent_1", "children": []},
#     {"name": "sub_agent_2", "children": []}
#   ]
# }
```

---

## API reference

### `Tracer`

```python
tracer = Tracer()                        # generates a new trace_id
tracer = Tracer(trace_id="abcdef...")    # use an existing trace_id
```

**`start_span(name, parent_span_id=None)`**

Returns a context manager. On `__enter__`, pushes the span onto the thread-local stack and returns it. On `__exit__`, closes the span, pops the stack, and records it.

Parent resolution order:
1. Explicit `parent_span_id` argument.
2. Current top-of-stack span for this thread (automatic nesting).
3. Remote parent set via `from_context()`.

```python
with tracer.start_span("my_op") as span:
    span.set_attribute("k", "v")
```

**`get_context()`**

Returns a serializable dict with the current trace and span IDs. Pass this to another process/agent to continue the same trace.

```python
ctx = tracer.get_context()
# {"trace_id": "...", "span_id": "...", "baggage": {}}
```

**`Tracer.from_context(ctx)`**

Class method. Creates a new Tracer with the same trace_id. The first span opened on this tracer will have `parent_span_id` set to `ctx["span_id"]`.

```python
child_tracer = Tracer.from_context(ctx)
with child_tracer.start_span("remote_op") as span:
    ...  # span.parent_span_id == ctx["span_id"]
```

**`get_spans()`**

Returns a list of completed span dicts. Active (open) spans are not included.

**`export_jsonl(path)`**

Appends each completed span as a JSON line to `path`.

**`get_trace_tree()`**

Reconstructs the parent-child hierarchy from completed spans. Returns a nested dict where each node has a `children` list.

---

### `Span`

Returned by `tracer.start_span()`. All methods can be called inside the `with` block.

**`set_attribute(key, value)`** — store a key-value pair (any JSON-serializable value).

**`add_event(name, attributes=None)`** — record a timestamped event.

**`record_error(exc)`** — set `status = "error"`, store `error_message`, add an error event with `exception.type`.

**`to_dict()`** — return a JSON-serializable dict of the full span.

Fields: `span_id` (8-char hex), `trace_id` (16-char hex), `parent_span_id`, `name`, `start_time`, `end_time`, `attributes`, `events`, `status` ("ok" or "error"), `error_message`.

---

### `trace_span` decorator

Works on sync and async functions. Auto-creates a tracer if none is active, or reuses the current one.

```python
@trace_span
def fetch_documents(query: str) -> list:
    ...

@trace_span("custom_span_name")
async def async_agent(prompt: str) -> str:
    ...
```

Both forms (`@trace_span` and `@trace_span("name")`) are supported.

---

### Module-level context functions

```python
from agent_trace import get_current_span, get_current_tracer

span = get_current_span()      # innermost active span for this thread, or None
tracer = get_current_tracer()  # active tracer for this thread, or None
```

---

## Context propagation between processes

```python
# Process A — coordinator
tracer = Tracer()
with tracer.start_span("coordinator") as span:
    ctx = tracer.get_context()
    # Send ctx to Process B via HTTP header, queue message, etc.
    response = call_remote_agent(payload, headers={"X-Trace-Context": json.dumps(ctx)})

# Process B — sub-agent
import json
ctx = json.loads(request.headers["X-Trace-Context"])
tracer = Tracer.from_context(ctx)
with tracer.start_span("sub_agent") as span:
    # span.parent_span_id == coordinator's span_id
    span.set_attribute("model", "gpt-4o")
    result = do_work()

tracer.export_jsonl("/var/log/traces.jsonl")
```

Both sides write JSONL to the same log sink. The trace_id is shared, so you can join them.

---

## Exporting and analyzing traces

```python
tracer.export_jsonl("traces.jsonl")
```

Each line is a complete span dict:

```json
{"span_id": "a1b2c3d4", "trace_id": "deadbeef01234567", "parent_span_id": null, "name": "coordinator", "start_time": 1741392000.1, "end_time": 1741392001.3, "attributes": {"model": "claude-sonnet-4-6", "input_tokens": 800}, "events": [], "status": "ok", "error_message": null}
{"span_id": "e5f6a7b8", "trace_id": "deadbeef01234567", "parent_span_id": "a1b2c3d4", "name": "sub_agent_1", "start_time": 1741392000.2, "end_time": 1741392000.9, "attributes": {"task": "fetch_documents"}, "events": [{"name": "tool_call", "timestamp": 1741392000.5, "attributes": {"tool": "search"}}], "status": "ok", "error_message": null}
```

Read them back:

```python
from agent_trace import read_jsonl

spans = read_jsonl("traces.jsonl")
errors = [s for s in spans if s["status"] == "error"]
slowest = max(spans, key=lambda s: (s["end_time"] or 0) - s["start_time"])
```

Rebuild the tree from a JSONL file (spans from multiple processes, same trace):

```python
from agent_trace import Tracer, read_jsonl
from agent_trace.span import Span

spans = read_jsonl("traces.jsonl")
# Reconstruct tree manually from the dicts if needed,
# or pass same trace_id to a fresh Tracer and re-run get_trace_tree()
# after populating _completed_spans from the JSONL data.
```

---

## License

MIT
