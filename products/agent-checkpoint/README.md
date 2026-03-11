# agent-checkpoint

Zero-dep agent state persistence. Save checkpoints, resume after failure, rollback to any point. Fixes "agentic amnesia" — agents that lose context and restart from scratch.

```bash
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-checkpoint
```

## When you need this

Your 10-step agent task fails at step 7. It restarts from step 1. Three hours of API calls, wasted.

Your agent runs for 2 hours, loses context mid-task, and re-implements work it already completed.

You need to test a risky operation but have no way to "undo" and try a different approach.

`agent-checkpoint` is disk-based state persistence for agent tasks. Zero deps. Human-readable JSON.

## Quick start

```python
from agent_checkpoint import CheckpointStore

store = CheckpointStore()  # saves to ~/.cache/agent-checkpoint/

# Save state
state = {"step": 1, "messages": [...], "results": []}
cp = store.save(state, label="step_1_complete")

# Later: restore
checkpoint = store.restore(cp.checkpoint_id)
state = checkpoint.state

# Or restore the latest
latest = store.latest()
```

## Resume after failure

```python
from agent_checkpoint import CheckpointStore, CheckpointRunner

store = CheckpointStore()
runner = CheckpointRunner(store)

@runner.task
def analyze_codebase(state: dict) -> dict:
    # Step 1 — save checkpoint before risky operation
    state["files"] = scan_files(state["path"])
    runner.checkpoint(state, "files_scanned")

    # Step 2 — another checkpoint
    state["analysis"] = analyze_files(state["files"])
    runner.checkpoint(state, "analysis_done")

    return state

# First run
result = runner.run({"path": "/src"})

# If it crashed at step 2, resume from step 1's checkpoint:
result = runner.resume(from_label="files_scanned")
# → runs from step 2 onward, no need to re-scan files
```

## Checkpointing message history

The most common agent state is a list of messages:

```python
store = CheckpointStore(path="./task_checkpoints")

# Save after each assistant response
for i, message in enumerate(agent.run(task)):
    state["messages"].append(message)
    if i % 5 == 0:  # checkpoint every 5 messages
        store.save(state, label=f"step_{i}")

# Resume after crash
checkpoint = store.latest()
agent.continue_from(checkpoint.state["messages"])
```

## Find and restore specific checkpoints

```python
# Latest checkpoint with a specific label
cp = store.latest_labeled("before_api_call")

# All checkpoints with a label (newest first)
checkpoints = store.find_by_label("step_1")

# Full history
for cp in store.list():
    print(cp)  # Checkpoint(id=a1b2c3d4, label='step_1', at=2026-03-11 18:30:00)
```

## Branching history

```python
# Save parent checkpoint
parent = store.save(state, label="before_experiment")

# Try approach A
state_a = dict(state)
state_a["approach"] = "A"
# ... run experiment A
cp_a = store.save(state_a, label="approach_A", parent_id=parent.checkpoint_id)

# Roll back and try approach B
state_b = store.restore(parent.checkpoint_id).state
state_b["approach"] = "B"
cp_b = store.save(state_b, label="approach_B", parent_id=parent.checkpoint_id)
```

## Checkpoint metadata

```python
cp = store.save(
    state,
    label="step_3",
    metadata={
        "session_id": session_id,
        "model": "claude-sonnet-4-6",
        "task": "analyze security vulnerabilities",
        "tokens_used": 15000,
    }
)

# Query metadata later
checkpoint = store.restore(cp.checkpoint_id)
print(checkpoint.metadata["tokens_used"])
```

## Storage and pruning

```python
store = CheckpointStore(
    path="./my_checkpoints",  # custom directory (default: ~/.cache/agent-checkpoint/)
    max_checkpoints=50,       # prune oldest when over limit (default: 100)
)
```

Each checkpoint is a single JSON file. Human-readable. Committal as text. The index is a single `index.json` file.

```
~/.cache/agent-checkpoint/
  index.json              ← checkpoint index
  a1b2c3d4e5f6a7b8.json  ← checkpoint data
  b9c0d1e2f3a4b5c6.json  ← checkpoint data
  ...
```

## Pairs well with

- **[agent-gate](../agent-gate)** — approve irreversible actions before they happen; checkpoint lets you rollback if they go wrong
- **[agent-log](../agent-log)** — log agent decisions; checkpoint saves the state those decisions led to
- **[agent-constraints](../agent-constraints)** — enforce rules; checkpoint lets you recover when a violation occurs

## Zero dependencies

Pure Python stdlib. Checkpoints are plain JSON files.

## License

MIT
