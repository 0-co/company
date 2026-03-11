# agent-constraints

Enforce rules on AI agent tool calls at the Python level, not the prompt level. When a constraint fails, execution stops before the tool runs — the agent cannot bypass it.

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-constraints
```

## The problem this solves

On Hacker News (Feb 2026), developer `buschleague` described what's now called "constraint self-bypass":

> "The agent would identify the module that was blocking completion and, instead of fixing the error, it would access the enforcement module and adjust the code to unblock itself."

Prompt-based constraints ("don't delete files" in the system prompt) can drift and be bypassed. They live in the agent's context window, and the agent can reason around them. Code-based constraints enforced at execution time cannot be bypassed — they're in your code, not the agent's context.

## Quick start

```python
from agent_constraints import ConstraintEnforcer, ConstraintViolation

enforcer = ConstraintEnforcer()

@enforcer.add(tools=["bash"])
def no_file_deletion(tool: str, args: dict) -> bool:
    cmd = args.get("command", "")
    return "rm -rf" not in cmd and "rm -r" not in cmd

@enforcer.add(tools=["read_file", "write_file"])
def no_credential_access(tool: str, args: dict) -> bool:
    path = args.get("path", "")
    return not any(p in path for p in [".env", ".ssh/id_rsa", ".aws/credentials", "/etc/passwd"])

# Wrap your tool functions
@enforcer.protect("bash")
def run_bash(command: str) -> str:
    return subprocess.run(command, shell=True, capture_output=True).stdout.decode()

# Now the agent cannot bypass these rules, even if it tries
try:
    run_bash("rm -rf /")
except ConstraintViolation as e:
    print(f"Blocked: {e.constraint_name}")  # no_file_deletion
```

## Constraint function signatures

```python
# Full signature
@enforcer.add
def my_constraint(tool: str, args: dict) -> bool:
    ...

# Args only
@enforcer.add
def my_constraint(args: dict) -> bool:
    ...

# No args (global rule)
@enforcer.add
def my_constraint() -> bool:
    ...

# Return a reason string
@enforcer.add
def my_constraint(tool, args) -> tuple[bool, str]:
    if "bad" in args.get("command", ""):
        return False, "Command contains 'bad'"
    return True, ""
```

## Wrapping tools

```python
# Decorator form
@enforcer.protect("bash")
def run_bash(command: str) -> str: ...

# Function form
checked_bash = enforcer.protect_fn("bash", run_bash)

# Dict of tools (common in agent frameworks)
tools = enforcer.protect_all({
    "bash": lambda args: run_bash(**args),
    "read_file": lambda args: open(args["path"]).read(),
    "write_file": lambda args: Path(args["path"]).write_text(args["content"]),
})
```

## Log-only mode

```python
# Don't block — just log violations
enforcer = ConstraintEnforcer(raises=False)

# Or per-constraint
@enforcer.add(raises=False)
def soft_constraint(tool, args):
    return "preferred" in args.get("command", "")

# Check violations after the fact
violations = enforcer.log.violations
print(f"{len(violations)} constraints violated")
```

## Tool filtering

```python
# Only apply to specific tools
@enforcer.add(tools=["bash", "run_command"])
def shell_constraint(tool, args):
    ...

# Remove a constraint at runtime
enforcer.remove("shell_constraint")
```

## Why this works when prompts don't

The constraints are Python functions in your code. The agent:
- Cannot see them (they're not in the context window)
- Cannot modify them (they're not in the agent's memory)
- Cannot reason around them (they run before the tool, not after)
- Cannot pass args to "disable" them (the check is unconditional)

The agent can only interact with constraints by... not violating them.

## Violation log

```python
enforcer.log.violations   # all failed checks (including log-only)
enforcer.log.blocked      # failed checks that raised ConstraintViolation
enforcer.log.all_events   # every check (pass + fail)

v = enforcer.log.violations[0]
print(v["constraint"])   # constraint name
print(v["tool"])         # tool that was called
print(v["args"])         # args that triggered the violation
print(v["blocked"])      # True if call was stopped
print(v["timestamp"])    # unix timestamp
```

## With the Claude Agent SDK

```python
# Define tools with constraints
enforcer = ConstraintEnforcer()

@enforcer.add(tools=["bash"])
def no_network_calls(tool, args):
    cmd = args.get("command", "")
    return not any(c in cmd for c in ["curl", "wget", "nc ", "ssh "])

# Wrap tools before passing to agent
tools = enforcer.protect_all({
    "bash": run_bash,
    "read_file": read_file,
})

# Agent gets constrained tools — cannot bypass
result = agent.run(task, tools=tools)
```

## Pairs well with

- **[agent-gate](../agent-gate)** — human approval for irreversible actions (complementary: gate = human-in-loop, constraints = code-in-loop)
- **[agent-log](../agent-log)** — log constraint violations alongside agent decisions
- **[agent-shield](../agent-shield)** — scan for malicious skills before loading them

## Zero dependencies

Pure Python stdlib. No frameworks required. Works with any agent library.

## License

MIT
