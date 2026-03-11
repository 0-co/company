"""agent-checkpoint — save and restore agent state between sessions."""

import hashlib
import json
import os
import shutil
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union


class CheckpointError(Exception):
    """Raised when a checkpoint operation fails."""
    pass


class Checkpoint:
    """A single saved state snapshot."""

    def __init__(
        self,
        checkpoint_id: str,
        label: str,
        state: Dict,
        metadata: Dict,
        created_at: float,
        parent_id: Optional[str] = None,
    ):
        self.checkpoint_id = checkpoint_id
        self.label = label
        self.state = state
        self.metadata = metadata
        self.created_at = created_at
        self.parent_id = parent_id

    def to_dict(self) -> Dict:
        return {
            "checkpoint_id": self.checkpoint_id,
            "label": self.label,
            "state": self.state,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "parent_id": self.parent_id,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "Checkpoint":
        return cls(
            checkpoint_id=d["checkpoint_id"],
            label=d.get("label", ""),
            state=d.get("state", {}),
            metadata=d.get("metadata", {}),
            created_at=d.get("created_at", 0.0),
            parent_id=d.get("parent_id"),
        )

    def __repr__(self) -> str:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.created_at))
        return f"Checkpoint(id={self.checkpoint_id[:8]}, label={self.label!r}, at={ts})"


def _make_checkpoint_id(state: Dict, label: str, ts: float) -> str:
    """Generate a deterministic checkpoint ID."""
    content = json.dumps({"state": state, "label": label, "ts": ts}, sort_keys=True, default=str)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


class CheckpointStore:
    """
    Persists agent checkpoints to disk. Manages a linear or branching
    history of state snapshots.

    Args:
        path: Directory to store checkpoints (default: ~/.cache/agent-checkpoint/)
        max_checkpoints: Maximum number of checkpoints to retain.
                         Oldest are pruned when limit is reached.
    """

    def __init__(
        self,
        path: Optional[str] = None,
        max_checkpoints: int = 100,
    ):
        if path is None:
            path = os.path.expanduser("~/.cache/agent-checkpoint")
        self._dir = Path(path)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._index_path = self._dir / "index.json"
        self._max_checkpoints = max_checkpoints
        self._index: Dict[str, Dict] = {}  # checkpoint_id → entry
        self._load_index()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save(
        self,
        state: Dict,
        label: str = "",
        metadata: Optional[Dict] = None,
        parent_id: Optional[str] = None,
    ) -> Checkpoint:
        """
        Save a state snapshot.

        Args:
            state: JSON-serializable dict to save.
            label: Human-readable label (e.g., "before_api_call", "step_3_complete").
            metadata: Optional additional info (task name, session ID, etc.)
            parent_id: ID of the parent checkpoint for branching history.

        Returns:
            The saved Checkpoint object.
        """
        ts = time.time()
        cid = _make_checkpoint_id(state, label, ts)
        checkpoint = Checkpoint(
            checkpoint_id=cid,
            label=label,
            state=state,
            metadata=metadata or {},
            created_at=ts,
            parent_id=parent_id,
        )
        self._write_checkpoint(checkpoint)
        self._index[cid] = {"label": label, "created_at": ts, "parent_id": parent_id}
        self._prune()
        self._save_index()
        return checkpoint

    def restore(self, checkpoint_id: str) -> Checkpoint:
        """
        Load a checkpoint by ID.

        Args:
            checkpoint_id: Full ID or 8-char prefix.

        Returns:
            The Checkpoint with its full state.

        Raises:
            CheckpointError if not found.
        """
        cid = self._resolve_id(checkpoint_id)
        return self._read_checkpoint(cid)

    def latest(self) -> Optional[Checkpoint]:
        """Return the most recently saved checkpoint, or None if empty."""
        if not self._index:
            return None
        latest_id = max(self._index, key=lambda k: self._index[k]["created_at"])
        return self._read_checkpoint(latest_id)

    def list(self) -> List[Checkpoint]:
        """Return all checkpoints, ordered newest first."""
        checkpoints = []
        for cid in sorted(self._index, key=lambda k: self._index[k]["created_at"], reverse=True):
            try:
                checkpoints.append(self._read_checkpoint(cid))
            except CheckpointError:
                pass  # corrupt entry — skip
        return checkpoints

    def delete(self, checkpoint_id: str) -> bool:
        """Delete a checkpoint. Returns True if found and deleted."""
        try:
            cid = self._resolve_id(checkpoint_id)
        except CheckpointError:
            return False
        path = self._dir / f"{cid}.json"
        if path.exists():
            path.unlink()
        if cid in self._index:
            del self._index[cid]
            self._save_index()
            return True
        return False

    def clear(self) -> None:
        """Delete all checkpoints."""
        for cid in list(self._index.keys()):
            path = self._dir / f"{cid}.json"
            if path.exists():
                path.unlink()
        self._index.clear()
        self._save_index()

    def find_by_label(self, label: str) -> List[Checkpoint]:
        """Return all checkpoints with the given label, newest first."""
        results = []
        for cid, entry in sorted(
            self._index.items(), key=lambda kv: kv[1]["created_at"], reverse=True
        ):
            if entry.get("label") == label:
                try:
                    results.append(self._read_checkpoint(cid))
                except CheckpointError:
                    pass
        return results

    def latest_labeled(self, label: str) -> Optional[Checkpoint]:
        """Return the most recent checkpoint with the given label."""
        matches = self.find_by_label(label)
        return matches[0] if matches else None

    def __len__(self) -> int:
        return len(self._index)

    def __repr__(self) -> str:
        return f"CheckpointStore(path={self._dir}, checkpoints={len(self._index)})"

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _resolve_id(self, checkpoint_id: str) -> str:
        """Resolve a full or prefix ID to a full checkpoint ID."""
        if checkpoint_id in self._index:
            return checkpoint_id
        # Try prefix match
        matches = [cid for cid in self._index if cid.startswith(checkpoint_id)]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise CheckpointError(
                f"Ambiguous checkpoint ID prefix '{checkpoint_id}': "
                f"matches {len(matches)} checkpoints"
            )
        raise CheckpointError(f"Checkpoint not found: {checkpoint_id!r}")

    def _checkpoint_path(self, cid: str) -> Path:
        return self._dir / f"{cid}.json"

    def _write_checkpoint(self, checkpoint: Checkpoint) -> None:
        path = self._checkpoint_path(checkpoint.checkpoint_id)
        tmp = path.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(checkpoint.to_dict(), f, separators=(",", ":"), default=str)
        tmp.replace(path)

    def _read_checkpoint(self, cid: str) -> Checkpoint:
        path = self._checkpoint_path(cid)
        if not path.exists():
            raise CheckpointError(f"Checkpoint file missing: {path}")
        try:
            with open(path) as f:
                data = json.load(f)
            return Checkpoint.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            raise CheckpointError(f"Corrupt checkpoint {cid[:8]}: {e}")

    def _load_index(self) -> None:
        if self._index_path.exists():
            try:
                with open(self._index_path) as f:
                    self._index = json.load(f)
            except (json.JSONDecodeError, KeyError):
                self._index = {}

    def _save_index(self) -> None:
        tmp = self._index_path.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(self._index, f, separators=(",", ":"))
        tmp.replace(self._index_path)

    def _prune(self) -> None:
        """Remove oldest checkpoints when over limit."""
        if len(self._index) <= self._max_checkpoints:
            return
        sorted_ids = sorted(self._index, key=lambda k: self._index[k]["created_at"])
        to_remove = sorted_ids[:len(self._index) - self._max_checkpoints]
        for cid in to_remove:
            self.delete(cid)


class CheckpointRunner:
    """
    Wraps an agent task with automatic checkpointing and resume-on-failure.

    Saves checkpoints at regular intervals or on demand. If the task fails,
    calling .resume() picks up from the last checkpoint.

    Usage::

        store = CheckpointStore()
        runner = CheckpointRunner(store)

        @runner.task
        def my_agent_task(state: dict) -> dict:
            state["step"] = 1
            runner.checkpoint(state, "step_1_done")

            state["step"] = 2
            runner.checkpoint(state, "step_2_done")

            return state

        # Run
        result = runner.run({"task": "analyze data"})

        # If it crashes and you want to resume:
        result = runner.resume()

    """

    def __init__(self, store: CheckpointStore):
        self._store = store
        self._task_fn: Optional[Callable] = None
        self._current_state: Optional[Dict] = None

    def task(self, fn: Callable) -> Callable:
        """Decorator to register the agent task function."""
        self._task_fn = fn
        return fn

    def checkpoint(self, state: Dict, label: str = "", metadata: Optional[Dict] = None) -> Checkpoint:
        """Save a checkpoint from within the running task."""
        self._current_state = state
        return self._store.save(state, label=label, metadata=metadata)

    def run(self, initial_state: Dict) -> Dict:
        """
        Run the task from initial_state. Saves a checkpoint before starting.
        Returns the final state.
        """
        if self._task_fn is None:
            raise CheckpointError("No task function registered. Use @runner.task")
        self._store.save(initial_state, label="__initial__")
        return self._task_fn(initial_state)

    def resume(self, from_label: Optional[str] = None) -> Dict:
        """
        Resume from the last checkpoint (or the checkpoint with from_label).
        """
        if self._task_fn is None:
            raise CheckpointError("No task function registered. Use @runner.task")
        if from_label:
            cp = self._store.latest_labeled(from_label)
            if cp is None:
                raise CheckpointError(f"No checkpoint found with label '{from_label}'")
        else:
            cp = self._store.latest()
            if cp is None:
                raise CheckpointError("No checkpoints found. Run first.")
        return self._task_fn(dict(cp.state))
