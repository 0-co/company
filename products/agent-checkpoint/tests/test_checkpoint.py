"""Tests for agent-checkpoint."""

import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_checkpoint import CheckpointStore, Checkpoint, CheckpointRunner, CheckpointError
from agent_checkpoint.checkpoint import _make_checkpoint_id


# ---------------------------------------------------------------------------
# _make_checkpoint_id
# ---------------------------------------------------------------------------

class TestMakeCheckpointId(unittest.TestCase):
    def test_deterministic(self):
        id1 = _make_checkpoint_id({"x": 1}, "label", 100.0)
        id2 = _make_checkpoint_id({"x": 1}, "label", 100.0)
        self.assertEqual(id1, id2)

    def test_different_state_different_id(self):
        id1 = _make_checkpoint_id({"x": 1}, "label", 100.0)
        id2 = _make_checkpoint_id({"x": 2}, "label", 100.0)
        self.assertNotEqual(id1, id2)

    def test_returns_16_chars(self):
        cid = _make_checkpoint_id({}, "", 0)
        self.assertEqual(len(cid), 16)


# ---------------------------------------------------------------------------
# Checkpoint serialization
# ---------------------------------------------------------------------------

class TestCheckpointSerialization(unittest.TestCase):
    def test_round_trip(self):
        cp = Checkpoint(
            checkpoint_id="abcd1234efgh5678",
            label="test",
            state={"step": 1, "data": [1, 2, 3]},
            metadata={"session": "abc"},
            created_at=1000.0,
            parent_id="parent123",
        )
        d = cp.to_dict()
        restored = Checkpoint.from_dict(d)
        self.assertEqual(restored.checkpoint_id, "abcd1234efgh5678")
        self.assertEqual(restored.label, "test")
        self.assertEqual(restored.state, {"step": 1, "data": [1, 2, 3]})
        self.assertEqual(restored.metadata, {"session": "abc"})
        self.assertAlmostEqual(restored.created_at, 1000.0)
        self.assertEqual(restored.parent_id, "parent123")

    def test_repr(self):
        cp = Checkpoint("abcd1234efgh5678", "mylabel", {}, {}, 0.0)
        r = repr(cp)
        self.assertIn("Checkpoint", r)
        self.assertIn("abcd1234", r)
        self.assertIn("mylabel", r)


# ---------------------------------------------------------------------------
# CheckpointStore basic operations
# ---------------------------------------------------------------------------

class TestCheckpointStore(unittest.TestCase):
    def _store(self, **kwargs) -> CheckpointStore:
        return CheckpointStore(path=tempfile.mkdtemp(), **kwargs)

    def test_save_and_restore(self):
        store = self._store()
        state = {"step": 1, "messages": [{"role": "user", "content": "hello"}]}
        cp = store.save(state, label="step_1")

        restored = store.restore(cp.checkpoint_id)
        self.assertEqual(restored.state, state)
        self.assertEqual(restored.label, "step_1")

    def test_restore_by_prefix(self):
        store = self._store()
        state = {"x": 1}
        cp = store.save(state)
        prefix = cp.checkpoint_id[:4]

        restored = store.restore(prefix)
        self.assertEqual(restored.state, state)

    def test_restore_not_found_raises(self):
        store = self._store()
        with self.assertRaises(CheckpointError):
            store.restore("nonexistent")

    def test_restore_ambiguous_prefix_raises(self):
        store = self._store()
        # Save states with similar hashes is hard to force, but we can mock:
        # Instead test that ambiguity is detected via the index
        store._index = {"ab123456": {}, "ab789012": {}}
        with self.assertRaises(CheckpointError) as ctx:
            store._resolve_id("ab")
        self.assertIn("Ambiguous", str(ctx.exception))

    def test_latest_returns_most_recent(self):
        store = self._store()
        cp1 = store.save({"step": 1})
        time.sleep(0.01)
        cp2 = store.save({"step": 2})

        latest = store.latest()
        self.assertEqual(latest.checkpoint_id, cp2.checkpoint_id)

    def test_latest_empty_store(self):
        store = self._store()
        self.assertIsNone(store.latest())

    def test_list_ordered_newest_first(self):
        store = self._store()
        cp1 = store.save({"n": 1})
        time.sleep(0.01)
        cp2 = store.save({"n": 2})
        time.sleep(0.01)
        cp3 = store.save({"n": 3})

        checkpoints = store.list()
        self.assertEqual(len(checkpoints), 3)
        self.assertEqual(checkpoints[0].checkpoint_id, cp3.checkpoint_id)
        self.assertEqual(checkpoints[2].checkpoint_id, cp1.checkpoint_id)

    def test_delete(self):
        store = self._store()
        cp = store.save({"x": 1})
        self.assertTrue(store.delete(cp.checkpoint_id))
        self.assertFalse(store.delete(cp.checkpoint_id))
        self.assertEqual(len(store), 0)

    def test_clear(self):
        store = self._store()
        store.save({"x": 1})
        store.save({"x": 2})
        store.clear()
        self.assertEqual(len(store), 0)
        self.assertIsNone(store.latest())

    def test_find_by_label(self):
        store = self._store()
        store.save({"x": 1}, label="step_1")
        store.save({"x": 2}, label="step_2")
        store.save({"x": 3}, label="step_1")

        results = store.find_by_label("step_1")
        self.assertEqual(len(results), 2)
        # newest first
        self.assertEqual(results[0].state["x"], 3)

    def test_latest_labeled(self):
        store = self._store()
        store.save({"x": 1}, label="step_1")
        time.sleep(0.01)
        store.save({"x": 2}, label="step_1")

        latest = store.latest_labeled("step_1")
        self.assertEqual(latest.state["x"], 2)

    def test_latest_labeled_not_found(self):
        store = self._store()
        self.assertIsNone(store.latest_labeled("nonexistent"))

    def test_metadata_preserved(self):
        store = self._store()
        meta = {"session": "abc123", "task": "analyze"}
        cp = store.save({"x": 1}, metadata=meta)
        restored = store.restore(cp.checkpoint_id)
        self.assertEqual(restored.metadata, meta)

    def test_parent_id_preserved(self):
        store = self._store()
        parent = store.save({"step": 1})
        child = store.save({"step": 2}, parent_id=parent.checkpoint_id)
        restored = store.restore(child.checkpoint_id)
        self.assertEqual(restored.parent_id, parent.checkpoint_id)

    def test_max_checkpoints_pruning(self):
        store = self._store(max_checkpoints=3)
        for i in range(5):
            store.save({"n": i})
            time.sleep(0.01)
        self.assertEqual(len(store), 3)
        # Newest 3 retained
        labels = [cp.state["n"] for cp in store.list()]
        self.assertEqual(sorted(labels, reverse=True), [4, 3, 2])

    def test_persistence(self):
        d = tempfile.mkdtemp()
        store1 = CheckpointStore(path=d)
        cp = store1.save({"x": 42}, label="persisted")

        store2 = CheckpointStore(path=d)
        restored = store2.restore(cp.checkpoint_id)
        self.assertEqual(restored.state["x"], 42)

    def test_len(self):
        store = self._store()
        self.assertEqual(len(store), 0)
        store.save({"x": 1})
        store.save({"x": 2})
        self.assertEqual(len(store), 2)

    def test_repr(self):
        store = self._store()
        r = repr(store)
        self.assertIn("CheckpointStore", r)
        self.assertIn("checkpoints=0", r)

    def test_corrupt_checkpoint_file_skipped_in_list(self):
        store = self._store()
        cp = store.save({"x": 1})
        # Corrupt the file
        corrupt_path = store._checkpoint_path(cp.checkpoint_id)
        with open(corrupt_path, "w") as f:
            f.write("{invalid json")
        # list() should skip it without raising
        result = store.list()
        self.assertEqual(len(result), 0)

    def test_restore_corrupt_raises(self):
        store = self._store()
        cp = store.save({"x": 1})
        corrupt_path = store._checkpoint_path(cp.checkpoint_id)
        with open(corrupt_path, "w") as f:
            f.write("{bad json}")
        with self.assertRaises(CheckpointError):
            store.restore(cp.checkpoint_id)

    def test_complex_nested_state(self):
        store = self._store()
        state = {
            "messages": [
                {"role": "system", "content": "You are an agent."},
                {"role": "user", "content": "Start analysis."},
                {"role": "assistant", "content": "I'll analyze step by step."},
            ],
            "tools_called": ["read_file", "bash"],
            "step": 3,
            "metadata": {"session_id": "abc-123", "model": "claude-sonnet-4-6"},
        }
        cp = store.save(state, label="complex")
        restored = store.restore(cp.checkpoint_id)
        self.assertEqual(restored.state, state)


# ---------------------------------------------------------------------------
# CheckpointRunner
# ---------------------------------------------------------------------------

class TestCheckpointRunner(unittest.TestCase):
    def _store(self) -> CheckpointStore:
        return CheckpointStore(path=tempfile.mkdtemp())

    def test_run_executes_task(self):
        store = self._store()
        runner = CheckpointRunner(store)

        @runner.task
        def my_task(state):
            state["done"] = True
            return state

        result = runner.run({"x": 1})
        self.assertTrue(result["done"])

    def test_run_saves_initial_checkpoint(self):
        store = self._store()
        runner = CheckpointRunner(store)

        @runner.task
        def my_task(state):
            return state

        runner.run({"x": 1})
        # Initial checkpoint should be saved
        self.assertGreaterEqual(len(store), 1)
        latest = store.latest_labeled("__initial__")
        self.assertIsNotNone(latest)

    def test_checkpoint_saves_state(self):
        store = self._store()
        runner = CheckpointRunner(store)

        @runner.task
        def my_task(state):
            state["step"] = 1
            runner.checkpoint(state, "step_1")
            state["step"] = 2
            runner.checkpoint(state, "step_2")
            return state

        runner.run({"x": 0})

        cp_step1 = store.latest_labeled("step_1")
        cp_step2 = store.latest_labeled("step_2")
        self.assertEqual(cp_step1.state["step"], 1)
        self.assertEqual(cp_step2.state["step"], 2)

    def test_resume_from_latest(self):
        store = self._store()
        runner = CheckpointRunner(store)
        call_args = []

        @runner.task
        def my_task(state):
            call_args.append(dict(state))
            return state

        runner.run({"x": 1})
        runner.resume()

        self.assertEqual(len(call_args), 2)
        self.assertEqual(call_args[1], call_args[0])

    def test_resume_from_label(self):
        store = self._store()
        runner = CheckpointRunner(store)
        resumed_from = []

        @runner.task
        def my_task(state):
            resumed_from.append(state.get("label_state", "initial"))
            runner.checkpoint({"label_state": "checkpoint"}, "my_label")
            return state

        runner.run({"label_state": "initial"})
        runner.resume(from_label="my_label")

        self.assertEqual(resumed_from[-1], "checkpoint")

    def test_no_task_raises(self):
        store = self._store()
        runner = CheckpointRunner(store)
        with self.assertRaises(CheckpointError):
            runner.run({})

    def test_resume_empty_store_raises(self):
        store = self._store()
        runner = CheckpointRunner(store)

        @runner.task
        def my_task(state):
            return state

        with self.assertRaises(CheckpointError):
            runner.resume()

    def test_resume_missing_label_raises(self):
        store = self._store()
        runner = CheckpointRunner(store)

        @runner.task
        def my_task(state):
            return state

        runner.run({"x": 1})
        with self.assertRaises(CheckpointError):
            runner.resume(from_label="nonexistent_label")


if __name__ == "__main__":
    unittest.main()
