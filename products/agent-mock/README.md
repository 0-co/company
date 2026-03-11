# agent-mock

Zero-dep LLM response mocking for testing AI agents. Fixture mode, record mode, playback mode. No real API calls during tests.

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-mock
```

## When you need this

Your agent test suite hits the real Anthropic API on every run. That's $0.50/run, 3 seconds per call, and non-deterministic. `agent-mock` replaces API calls with fixtures — pre-defined responses or recorded real responses played back later.

- **Tests cost money**: every `pytest` run burns tokens
- **Tests are slow**: network latency on every assertion
- **Tests are flaky**: API errors, rate limits, and non-determinism break CI
- **You can't test error paths**: you can't make Anthropic return a 429 on demand

## Quick start

```python
import anthropic
from agent_mock import MockSession

session = MockSession()
session.on(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "classify this email"}],
    returns={
        "content": [{"type": "text", "text": "spam"}],
    },
)

client = session.wrap(anthropic.Anthropic())
response = client.messages.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "classify this email"}],
)
assert response.content[0].text == "spam"
```

## Three modes

### Fixture mode — define responses manually

```python
session = MockSession()

# Simple response
session.on(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "hello"}],
    returns={"content": [{"type": "text", "text": "Hi!"}]},
)

# Multiple sequential responses (cycles, last one repeats)
session.on(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "next step?"}],
    returns=[
        {"content": [{"type": "text", "text": "Step 1: ..."}]},
        {"content": [{"type": "text", "text": "Step 2: ..."}]},
    ],
)

# Raise an error (test error handling)
from agent_mock import MockError
session.on(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "trigger error"}],
    raises=MockError("Rate limited", status_code=429),
)
```

### Record mode — capture real responses once

```python
# Run once against real API, save to cassette
with MockSession.record("cassette.json") as session:
    client = session.wrap(anthropic.Anthropic())
    response = client.messages.create(...)  # real API call, saved to file
```

### Playback mode — replay without API calls

```python
# Every test run uses the cassette — zero API calls
with MockSession.playback("cassette.json") as session:
    client = session.wrap(anthropic.Anthropic())
    response = client.messages.create(...)  # served from cassette
```

## Strict mode

```python
# Raises MockError if a call has no matching fixture (default: pass through to real client)
session = MockSession(strict=True)
```

## Works with OpenAI too

```python
import openai
session = MockSession()
session.on(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "hi"}],
    returns={
        "choices": [{"message": {"role": "assistant", "content": "hello"}}],
    },
)
client = session.wrap(openai.OpenAI())
response = client.chat.completions.create(model="gpt-4o-mini", messages=[...])
```

Streaming calls (`stream=True`) bypass the mock and hit the real client.

## Response access

Mock responses use the same attribute structure as real SDK responses:

```python
# Anthropic
response.content[0].text
response.usage.input_tokens
response.model

# OpenAI
response.choices[0].message.content
```

## Side effects

```python
def dynamic_response(call_count: int):
    return types.SimpleNamespace(
        content=[types.SimpleNamespace(text=f"response {call_count}")]
    )

session.on(model="m", messages=[...], side_effect=dynamic_response)
```

## In a test suite

```python
import unittest
from agent_mock import MockSession, MockError

class TestMyAgent(unittest.TestCase):
    def setUp(self):
        self.session = MockSession()
        self.client = self.session.wrap(anthropic.Anthropic())

    def test_classifies_spam(self):
        self.session.on(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "Buy now!"}],
            returns={"content": [{"type": "text", "text": "spam"}]},
        )
        result = classify(self.client, "Buy now!")
        self.assertEqual(result, "spam")

    def test_handles_rate_limit(self):
        self.session.on(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "Buy now!"}],
            raises=MockError("Rate limited", status_code=429),
        )
        with self.assertRaises(MockError):
            classify(self.client, "Buy now!")
```

## Cassette file format

```json
{
  "interactions": [
    {
      "key": "<sha256 of request>",
      "request": {"model": "...", "messages": [...]},
      "response": {"content": [...], "usage": {...}}
    }
  ]
}
```

Human-readable JSON. Commit cassettes alongside tests. Check in CI.

## Pairs well with

- **[agent-eval](../agent-eval)** — write assertions on mocked responses
- **[agent-cache](../agent-cache)** — cache real responses in production; mock in tests
- **[agent-retry](../agent-retry)** — use `MockError(status_code=429)` to test retry logic

## Zero dependencies

Pure Python stdlib. No `httpx`, no `responses`, no `moto`. Cassettes are plain JSON files.

## License

MIT
