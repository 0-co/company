"""Tests for agent-constraints."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_constraints import ConstraintEnforcer, ConstraintViolation, ViolationLog


# ---------------------------------------------------------------------------
# Basic enforcement tests
# ---------------------------------------------------------------------------

class TestConstraintRegistration(unittest.TestCase):
    def test_add_decorator(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add
        def my_constraint(tool, args):
            return True

        self.assertIn("my_constraint", enforcer.constraint_names)
        self.assertEqual(len(enforcer), 1)

    def test_add_with_name(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add(name="custom_name")
        def fn(tool, args):
            return True

        self.assertIn("custom_name", enforcer.constraint_names)

    def test_add_with_tools_filter(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add(tools=["bash"])
        def only_bash(tool, args):
            return False  # always fail

        # check "bash" should raise
        with self.assertRaises(ConstraintViolation):
            enforcer.check("bash", {})

        # check "read_file" should pass (constraint doesn't apply)
        enforcer.check("read_file", {})  # no exception

    def test_remove_constraint(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: True, name="to_remove")
        self.assertTrue(enforcer.remove("to_remove"))
        self.assertFalse(enforcer.remove("nonexistent"))
        self.assertEqual(len(enforcer), 0)

    def test_clear_constraints(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: True, name="c1")
        enforcer.add(lambda t, a: True, name="c2")
        enforcer.clear()
        self.assertEqual(len(enforcer), 0)


class TestConstraintEnforcement(unittest.TestCase):
    def test_passes_when_all_constraints_pass(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: True, name="always_pass")
        enforcer.check("bash", {"command": "ls -la"})  # no exception

    def test_raises_when_constraint_fails(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: False, name="always_fail")
        with self.assertRaises(ConstraintViolation) as ctx:
            enforcer.check("bash", {"command": "rm -rf /"})
        self.assertEqual(ctx.exception.constraint_name, "always_fail")
        self.assertEqual(ctx.exception.tool, "bash")

    def test_violation_includes_tool_args(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: False, name="fail")
        try:
            enforcer.check("bash", {"command": "bad"})
        except ConstraintViolation as e:
            self.assertEqual(e.tool_args, {"command": "bad"})

    def test_log_only_mode(self):
        enforcer = ConstraintEnforcer(raises=False)
        enforcer.add(lambda t, a: False, name="log_only")
        enforcer.check("bash", {"command": "bad"})  # no exception
        self.assertEqual(len(enforcer.log), 1)

    def test_mixed_raise_and_log(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: False, name="log_this", raises=False)
        enforcer.add(lambda t, a: True, name="pass_this")
        enforcer.check("bash", {})  # log_this logs, pass_this passes
        self.assertEqual(len(enforcer.log), 1)
        self.assertEqual(enforcer.log.violations[0]["constraint"], "log_this")

    def test_multiple_constraints_first_fails(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: False, name="first_fail")
        enforcer.add(lambda t, a: False, name="second_fail")
        with self.assertRaises(ConstraintViolation) as ctx:
            enforcer.check("bash", {})
        # Should fail on first constraint
        self.assertEqual(ctx.exception.constraint_name, "first_fail")

    def test_custom_message(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: False, name="f", message="Custom violation message")
        try:
            enforcer.check("t", {})
        except ConstraintViolation as e:
            self.assertIn("Custom violation message", str(e))

    def test_constraint_that_returns_tuple(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add
        def with_reason(tool, args):
            return False, "Specific reason: no deletions"

        try:
            enforcer.check("t", {})
        except ConstraintViolation as e:
            self.assertIn("Specific reason", str(e))

    def test_constraint_raises_itself(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add
        def raises_directly(tool, args):
            raise ConstraintViolation("raises_directly", tool, args, "Direct raise")

        with self.assertRaises(ConstraintViolation) as ctx:
            enforcer.check("bash", {})
        self.assertIn("Direct raise", str(ctx.exception))

    def test_no_constraints_passes(self):
        enforcer = ConstraintEnforcer()
        enforcer.check("any_tool", {"any": "args"})  # no exception


# ---------------------------------------------------------------------------
# Constraint function signature variations
# ---------------------------------------------------------------------------

class TestConstraintSignatures(unittest.TestCase):
    def test_two_arg_signature(self):
        """fn(tool, args) -> bool"""
        enforcer = ConstraintEnforcer()
        calls = []

        def fn(tool, args):
            calls.append((tool, args))
            return True

        enforcer.add(fn, name="two_arg")
        enforcer.check("mytool", {"x": 1})
        self.assertEqual(calls, [("mytool", {"x": 1})])

    def test_one_arg_signature(self):
        """fn(args) -> bool"""
        enforcer = ConstraintEnforcer()
        calls = []

        def fn(args):
            calls.append(args)
            return True

        enforcer.add(fn, name="one_arg")
        enforcer.check("mytool", {"x": 1})
        self.assertEqual(calls, [{"x": 1}])

    def test_zero_arg_signature(self):
        """fn() -> bool"""
        enforcer = ConstraintEnforcer()
        calls = []

        def fn():
            calls.append(True)
            return True

        enforcer.add(fn, name="zero_arg")
        enforcer.check("mytool", {})
        self.assertEqual(calls, [True])

    def test_returns_none_treated_as_pass(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: None, name="none_return")
        enforcer.check("t", {})  # no exception


# ---------------------------------------------------------------------------
# protect() decorator tests
# ---------------------------------------------------------------------------

class TestProtectDecorator(unittest.TestCase):
    def test_protect_blocks_bad_calls(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add(tools=["bash"])
        def no_rm_rf(tool, args):
            return "rm -rf" not in args.get("command", "")

        call_count = [0]

        @enforcer.protect("bash")
        def run_bash(command):
            call_count[0] += 1
            return f"ran: {command}"

        # Good call passes
        result = run_bash("ls -la")
        self.assertEqual(result, "ran: ls -la")
        self.assertEqual(call_count[0], 1)

        # Bad call blocked
        with self.assertRaises(ConstraintViolation):
            run_bash("rm -rf /")
        self.assertEqual(call_count[0], 1)  # not called

    def test_protect_passes_kwargs(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: True, name="pass")

        results = []

        @enforcer.protect("mytool")
        def my_tool(x, y=10):
            results.append((x, y))

        my_tool(1, y=20)
        self.assertEqual(results, [(1, 20)])

    def test_protect_fn(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: a.get("safe", True), name="safe_check")

        call_count = [0]

        def inner(safe=True):
            call_count[0] += 1

        wrapped = enforcer.protect_fn("tool", inner)
        wrapped(safe=True)
        self.assertEqual(call_count[0], 1)

        with self.assertRaises(ConstraintViolation):
            wrapped(safe=False)
        self.assertEqual(call_count[0], 1)


# ---------------------------------------------------------------------------
# protect_all() tests
# ---------------------------------------------------------------------------

class TestProtectAll(unittest.TestCase):
    def test_protect_all_wraps_all_tools(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: t != "dangerous", name="no_dangerous")

        calls = []
        raw_tools = {
            "safe_tool": lambda args: calls.append(("safe", args)) or "ok",
            "dangerous": lambda args: calls.append(("danger", args)) or "bad",
        }
        tools = enforcer.protect_all(raw_tools)

        # safe_tool passes
        result = tools["safe_tool"]({"x": 1})
        self.assertEqual(result, "ok")
        self.assertEqual(calls, [("safe", {"x": 1})])

        # dangerous blocked
        with self.assertRaises(ConstraintViolation):
            tools["dangerous"]({"x": 1})
        self.assertEqual(len(calls), 1)  # dangerous not called

    def test_protect_all_returns_all_keys(self):
        enforcer = ConstraintEnforcer()
        raw_tools = {"a": lambda args: None, "b": lambda args: None}
        tools = enforcer.protect_all(raw_tools)
        self.assertEqual(set(tools.keys()), {"a", "b"})


# ---------------------------------------------------------------------------
# ViolationLog tests
# ---------------------------------------------------------------------------

class TestViolationLog(unittest.TestCase):
    def test_empty_log(self):
        log = ViolationLog()
        self.assertEqual(len(log), 0)
        self.assertEqual(log.violations, [])
        self.assertEqual(log.all_events, [])

    def test_records_violation(self):
        enforcer = ConstraintEnforcer(raises=False)
        enforcer.add(lambda t, a: False, name="v1")
        enforcer.check("bash", {"cmd": "bad"})

        self.assertEqual(len(enforcer.log), 1)
        v = enforcer.log.violations[0]
        self.assertEqual(v["constraint"], "v1")
        self.assertEqual(v["tool"], "bash")
        self.assertFalse(v["passed"])
        # raises=False means call was NOT blocked
        self.assertFalse(v["blocked"])

    def test_all_events_includes_passes(self):
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: True, name="pass_c")
        enforcer.check("bash", {})

        # No violations but event was recorded
        self.assertEqual(len(enforcer.log), 0)
        self.assertEqual(len(enforcer.log.all_events), 1)
        self.assertFalse(enforcer.log.all_events[0]["blocked"])

    def test_log_has_timestamp(self):
        enforcer = ConstraintEnforcer(raises=False)
        enforcer.add(lambda t, a: False, name="c")
        enforcer.check("t", {})
        self.assertIn("timestamp", enforcer.log.violations[0])
        self.assertGreater(enforcer.log.violations[0]["timestamp"], 0)

    def test_repr(self):
        log = ViolationLog()
        self.assertIn("ViolationLog", repr(log))


# ---------------------------------------------------------------------------
# Real-world constraint examples
# ---------------------------------------------------------------------------

class TestRealWorldConstraints(unittest.TestCase):
    def test_no_rm_rf(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add(tools=["bash"])
        def no_delete(tool, args):
            cmd = args.get("command", "")
            return "rm -rf" not in cmd and "rm -r" not in cmd

        enforcer.check("bash", {"command": "ls -la"})

        with self.assertRaises(ConstraintViolation):
            enforcer.check("bash", {"command": "rm -rf /"})

    def test_no_credential_files(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add(tools=["read_file", "write_file"])
        def no_secrets(tool, args):
            path = args.get("path", "")
            blocked = [".env", ".ssh/id_rsa", "/etc/passwd", ".aws/credentials"]
            return not any(b in path for b in blocked)

        enforcer.check("read_file", {"path": "/home/user/code/app.py"})

        with self.assertRaises(ConstraintViolation):
            enforcer.check("read_file", {"path": "/home/user/.env"})

    def test_rate_limit_constraint(self):
        """Log-only rate limit tracker."""
        import time
        call_times = []
        LIMIT = 3

        enforcer = ConstraintEnforcer()

        @enforcer.add(tools=["api_call"], raises=False)
        def rate_limit(tool, args):
            now = time.time()
            recent = [t for t in call_times if now - t < 1.0]
            call_times.append(now)
            return len(recent) < LIMIT, f"Rate limit: {len(recent)+1}/{LIMIT}"

        for _ in range(3):
            enforcer.check("api_call", {})

        # 4th call exceeds limit — logged but not raised (raises=False)
        enforcer.check("api_call", {})
        self.assertGreater(len(enforcer.log), 0)

    def test_max_tokens_constraint(self):
        enforcer = ConstraintEnforcer()

        @enforcer.add
        def max_tokens(tool, args):
            if tool in ("messages.create", "chat.completions.create"):
                return args.get("max_tokens", 0) <= 4096
            return True

        enforcer.check("messages.create", {"max_tokens": 1000})

        with self.assertRaises(ConstraintViolation):
            enforcer.check("messages.create", {"max_tokens": 10000})

    def test_constraint_self_bypass_not_possible(self):
        """
        The whole point: constraints live in Python, agent cannot bypass them.
        This test verifies that even if we pass args claiming to "disable" the
        constraint, it still fires.
        """
        enforcer = ConstraintEnforcer()
        enforcer.add(lambda t, a: False, name="cannot_be_bypassed")

        # Agent tries to pass args to disable constraint — doesn't work
        with self.assertRaises(ConstraintViolation):
            enforcer.check("bash", {
                "command": "ls",
                "disable_constraints": True,  # agent trick attempt
                "override_safety": True,       # another trick attempt
            })


# ---------------------------------------------------------------------------
# Repr tests
# ---------------------------------------------------------------------------

class TestRepr(unittest.TestCase):
    def test_enforcer_repr(self):
        enforcer = ConstraintEnforcer()
        r = repr(enforcer)
        self.assertIn("ConstraintEnforcer", r)
        self.assertIn("constraints=0", r)

    def test_violation_repr(self):
        v = ConstraintViolation("test_c", "bash", {}, "test message")
        self.assertIn("test message", str(v))


if __name__ == "__main__":
    unittest.main()
