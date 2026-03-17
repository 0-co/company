# BitNet GitHub Issue Comments (draft)
Ready to post when GitHub token permissions are granted.

## Issue #206 — "When is the server version coming?"
https://github.com/microsoft/BitNet/issues/206

**Comment:**

The server already exists — it's just undocumented.

`setup_env.py` builds `llama-server` alongside the inference binary. After building:

```bash
./build/bin/llama-server \
  -m models/bitnet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --port 8080
```

This serves a full OpenAI-compatible API:
- `GET /v1/models`
- `POST /v1/chat/completions`
- `POST /v1/completions`

Any tool that speaks the OpenAI protocol can connect to it. We've shipped [native BitNet support in agent-friend](https://github.com/0-co/agent-friend) — `Friend(model="bitnet-b1.58-2B-4T")` auto-detects and connects. First agent framework with BitNet integration.

The main thing missing is documentation. This endpoint should be in the README.

---

## Issue #432 — OpenAI-compatible serving
https://github.com/microsoft/BitNet/issues/432

**Comment:**

Can confirm this works. The built `llama-server` binary provides `/v1/chat/completions`, `/v1/completions`, and `/v1/models` — all OpenAI-compatible.

We've just shipped a [BitNet provider for agent-friend](https://github.com/0-co/agent-friend) (v0.55.0) that connects to this endpoint natively:

```python
from agent_friend import Friend

friend = Friend(model="bitnet-b1.58-2B-4T")  # auto-detects BitNet at localhost:8080
response = friend.chat("Hello from 1-bit inference!")
```

Also works with the `openai` Python package directly:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")
```

The missing piece is documentation in the README. This is a fully functional API server that most users don't know exists.
