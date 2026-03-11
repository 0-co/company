# agent-schema

Zero-dependency structured output validation for AI agents.

LLMs frequently return malformed JSON, wrong field types, or miss required fields.
`agent-schema` validates LLM responses against a schema and auto-retries with
the validation error fed back to the model — until it returns a valid response
or exhausts the retry budget.

## When you need this

- Your agent pipeline breaks because the LLM returned `{"score": "high"}` instead of `{"score": 85}`.
- You're tired of writing `try: json.loads(resp) except` blocks everywhere.
- The model wraps its JSON in a markdown code fence and your parser chokes.
- You want CI to fail if your agent can't reliably produce structured output.
- You need the above with **zero additional dependencies** — no Pydantic, no jsonschema.

## Installation

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-schema
```

## Quick start

### Validate a response

```python
from agent_schema import SchemaValidator

schema = {
    "type": "object",
    "required": ["name", "score"],
    "properties": {
        "name": {"type": "string"},
        "score": {"type": "number", "minimum": 0, "maximum": 100},
        "status": {"type": "string", "enum": ["pending", "done", "failed"]},
    },
}

validator = SchemaValidator()

# Validate a dict directly
result = validator.validate({"name": "Alice", "score": 95, "status": "done"}, schema)
print(result.valid)   # True
print(result.data)    # {'name': 'Alice', 'score': 95, 'status': 'done'}

# Validate raw LLM text (handles code fences, surrounding prose, etc.)
llm_output = """
Here is the result:
```json
{"name": "Bob", "score": 200}
```
"""
result = validator.parse_and_validate(llm_output, schema)
print(result.valid)   # False
print(result.errors)  # ["root.score: 200 is greater than maximum 100"]
```

### Extract JSON from messy output

```python
from agent_schema import JSONExtractor

extractor = JSONExtractor()

# Handles all common LLM output formats
text = 'Sure! Here is the data: {"items": [1, 2, 3], "total": 3}'
parsed = extractor.extract_and_parse(text)
# {'items': [1, 2, 3], 'total': 3}

text = '```json\n{"status": "ok"}\n```'
parsed = extractor.extract_and_parse(text)
# {'status': 'ok'}
```

### Auto-retry until valid (Anthropic)

```python
import anthropic
from agent_schema import RetrySchema, SchemaMaxRetriesExceeded

client = anthropic.Anthropic()

schema = {
    "type": "object",
    "required": ["sentiment", "confidence"],
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
    },
}

rs = RetrySchema(client, model="claude-3-5-haiku-latest", max_retries=3)

try:
    result = rs.complete(
        messages=[{"role": "user", "content": "Analyze: 'I love this product!'"}],
        schema=schema,
        system="Respond with JSON only.",
    )
    print(result)  # {'sentiment': 'positive', 'confidence': 0.95}
except SchemaMaxRetriesExceeded as e:
    print(f"Failed after {e.attempts} attempts: {e.last_errors}")
```

### Auto-retry until valid (OpenAI)

```python
from openai import OpenAI
from agent_schema import RetrySchema

client = OpenAI()
rs = RetrySchema(client, model="gpt-4o-mini", max_retries=3)

result = rs.complete(
    messages=[{"role": "user", "content": "Extract the entities from: 'Alice works at Acme Corp'"}],
    schema={
        "type": "object",
        "required": ["person", "organization"],
        "properties": {
            "person": {"type": "string"},
            "organization": {"type": "string"},
        },
    },
)
```

### Async support

```python
import asyncio
import anthropic
from agent_schema import RetrySchema

async def main():
    client = anthropic.AsyncAnthropic()
    rs = RetrySchema(client, model="claude-3-5-haiku-latest")
    result = await rs.acomplete(
        messages=[{"role": "user", "content": "..."}],
        schema=schema,
    )
    return result

asyncio.run(main())
```

## API reference

### `SchemaValidator`

```python
validator = SchemaValidator()

result = validator.validate(data: dict, schema: dict) -> ValidationResult
result = validator.parse_and_validate(text: str, schema: dict) -> ValidationResult
```

`ValidationResult` fields:
- `valid: bool`
- `errors: list[str]` — human-readable error messages
- `data: dict | None` — the parsed/validated data (None if invalid)

### Schema format

Simplified JSON Schema subset:

```python
{
    "type": "object",            # string | number | integer | boolean | array | object | null
    "required": ["field1"],      # list of required field names
    "properties": {
        "name":   {"type": "string", "minLength": 1, "maxLength": 100},
        "score":  {"type": "number", "minimum": 0, "maximum": 100},
        "count":  {"type": "integer"},
        "active": {"type": "boolean"},
        "tags":   {"type": "array", "items": {"type": "string"}},
        "meta":   {"type": "object"},
        "status": {"type": "string", "enum": ["a", "b", "c"]},
        "nothing":{"type": "null"},
    },
}
```

Supported constraints: `minimum`, `maximum`, `minLength`, `maxLength`, `enum`, `required`, `items`.

### `JSONExtractor`

```python
extractor = JSONExtractor()

raw_json: str | None = extractor.extract(text)
parsed: dict | list | None = extractor.extract_and_parse(text)
```

Extraction strategies (tried in order):
1. Direct JSON parse of the whole input.
2. Extract from ` ```json ... ``` ` fenced code block.
3. Extract from ` ``` ... ``` ` fenced code block.
4. Find first balanced `{ ... }` block.
5. Find first balanced `[ ... ]` block.

### `RetrySchema`

```python
rs = RetrySchema(client, model: str, max_retries: int = 3)

result: dict = rs.complete(messages: list, schema: dict, system: str = None)
result: dict = await rs.acomplete(messages: list, schema: dict, system: str = None)
```

Client detection:
- Anthropic: `hasattr(client, 'messages')` → calls `client.messages.create()`
- OpenAI: `hasattr(client, 'chat')` → calls `client.chat.completions.create()`

On validation failure, the retry loop appends to the conversation:
```
assistant: <invalid response>
user: "Your response had validation errors: <errors>. Please fix and respond with valid JSON only."
```

### Exceptions

```python
SchemaValidationError(errors: list[str], response: str)   # single-attempt failure
SchemaMaxRetriesExceeded(attempts: int, last_errors: list[str])  # exhausted retries
```

## Zero deps

Only Python stdlib: `json`, `re`, `dataclasses`, `typing`, `asyncio`.

Python 3.9+. MIT license.
