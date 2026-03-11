# agent-gate

AI agents make irreversible mistakes. They send the wrong email, delete the wrong file, post the wrong message. By the time you notice, it's done.

agent-gate adds a human approval step before irreversible agent actions. One line to add a gate. Raises `ActionDenied` if the human says no.

```python
from agent_gate import gate

gate.confirm("Send email to all users about the outage")
# → pauses, shows prompt, waits for y/N
```

Zero dependencies. Pure stdlib. Python 3.9+.

---

## When you need this

- **Destructive file operations** — agent about to delete files, truncate a database, or overwrite config
- **External communications** — sending emails, Slack messages, or webhooks to real users on behalf of the agent
- **Financial transactions** — any action that moves money or modifies billing
- **Production deploys** — `@gate.requires("Deploy {service} to production")` before the agent triggers a deploy
- **Agentic scaffolding** — wrap irreversible tool calls in a decorator, keep the rest fully autonomous
- **Testing** — use `AutoApproveHandler` or `AutoDenyHandler` in tests; `StdinApprovalHandler` in production

---

## Install

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-gate
```

---

## Quick start

### Direct confirmation

```python
from agent_gate import gate, ActionDenied

try:
    gate.confirm("Delete /var/data/production.db")
    os.remove("/var/data/production.db")
except ActionDenied as e:
    print(f"Cancelled: {e.action}")
```

Prompt shown to user:
```
[agent-gate] Action requires approval:
  Delete /var/data/production.db
  Approve? [y/N]
```

### Decorator

```python
from agent_gate import gate

@gate.requires("Send email to {to}", context={"subject": "{subject}"})
def send_email(to: str, subject: str, body: str) -> None:
    smtp.send(to, subject, body)

# Called normally — gate intercepts and asks for approval first
send_email("user@example.com", "Invoice due", body_text)
```

Action and context strings are interpolated with the function's arguments: `{to}` → `user@example.com`.

### Async

```python
@gate.requires("Post to Twitch chat: {message}")
async def post_chat(message: str) -> None:
    await twitch.send(message)
```

Works identically for async functions.

---

## Handlers

The handler controls how approval is requested. Pass it to `Gate()`:

### StdinApprovalHandler (default)

Prompts on stderr, reads from stdin. Interactive terminals only.

```python
from agent_gate import Gate, StdinApprovalHandler

gate = Gate(handler=StdinApprovalHandler(timeout=30))  # auto-deny after 30s
```

### AutoApproveHandler

Approves everything. Use in tests.

```python
from agent_gate import Gate, AutoApproveHandler

test_gate = Gate(handler=AutoApproveHandler())

@test_gate.requires("Send notification")
def notify(user_id: int) -> None:
    ...  # will execute in tests without prompting
```

### AutoDenyHandler

Denies everything. Use in CI or read-only contexts where actions must never fire.

```python
from agent_gate import Gate, AutoDenyHandler

ci_gate = Gate(handler=AutoDenyHandler())
```

### CallbackApprovalHandler

Delegates to a custom function. Wire up Slack DMs, webhooks, database policies, or anything else.

```python
from agent_gate import Gate, CallbackApprovalHandler

def my_approval(action: str, context: dict) -> bool:
    # Check a policy database, send a Slack message, etc.
    return policy_db.is_allowed(action)

gate = Gate(handler=CallbackApprovalHandler(my_approval))
```

---

## Configuration

```python
from agent_gate import Gate, GateConfig, StdinApprovalHandler

config = GateConfig(
    handler=StdinApprovalHandler(timeout=60),  # 60s before auto-deny
    log_decisions=True,    # print APPROVED/DENIED to stderr (default: True)
)

gate = Gate(config=config)
```

---

## Exceptions

```python
from agent_gate import ActionDenied, GateTimeout

# Raised when action is denied (user says N, or AutoDenyHandler)
ActionDenied:
    .action  # the action description
    .reason  # 'user_denied', 'timeout', 'auto_deny'

# Subclass of ActionDenied for timeouts
GateTimeout:
    .action
    .timeout  # the timeout duration that expired
```

---

## Patterns

### Risk-based gates

```python
import os
from agent_gate import Gate, AutoApproveHandler, StdinApprovalHandler

# Only gate high-risk actions; low-risk run freely
low_risk = Gate(handler=AutoApproveHandler())
high_risk = Gate(handler=StdinApprovalHandler(timeout=120))

@low_risk.requires("Read file {path}")
def read_file(path: str) -> str:
    return open(path).read()

@high_risk.requires("Delete file {path}")
def delete_file(path: str) -> None:
    os.remove(path)
```

### Context-aware decisions

```python
def policy_handler(action: str, context: dict) -> bool:
    # Auto-approve for non-production environments
    if os.environ.get("ENV") != "production":
        return True
    # Auto-deny anything touching billing
    if "billing" in action.lower():
        return False
    # Prompt for everything else
    return StdinApprovalHandler().request(action, context)
```

---

## How it works

`gate.confirm()` calls `handler.request(action, context)`. If it returns False, `ActionDenied` is raised. If True, execution continues.

The decorator wraps the function: on call, it binds the arguments, interpolates templates, calls `confirm()`, then executes the original function (or raises before execution).

No global state. Each Gate is independent. Thread-safe for StdinApprovalHandler (uses threading.Event to avoid blocking the event loop).

---

Built at [0co](https://github.com/0-co/company) — an AI autonomously running a startup.
