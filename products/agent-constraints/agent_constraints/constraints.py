"""agent-constraints — enforce rules at execution time, not prompt time."""

import functools
import inspect
import json
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


class ConstraintViolation(Exception):
    """Raised when a constraint is violated."""

    def __init__(self, constraint_name: str, tool: str, tool_args: Dict, message: str = ""):
        self.constraint_name = constraint_name
        self.tool = tool
        self.tool_args = tool_args
        self.message = message or f"Constraint '{constraint_name}' violated by tool '{tool}'"
        super().__init__(self.message)


class ViolationLog:
    """Append-only log of constraint violations."""

    def __init__(self):
        self._entries: List[Dict] = []

    def record(self, constraint: str, tool: str, args: Dict, passed: bool, blocked: bool) -> None:
        self._entries.append({
            "constraint": constraint,
            "tool": tool,
            "args": args,
            "passed": passed,
            "blocked": blocked,  # True = call was stopped (raised), False = allowed through
            "timestamp": time.time(),
        })

    @property
    def violations(self) -> List[Dict]:
        """All failed constraint checks (including log-only ones)."""
        return [e for e in self._entries if not e["passed"]]

    @property
    def blocked(self) -> List[Dict]:
        """Constraint failures that stopped execution (raised=True)."""
        return [e for e in self._entries if e["blocked"]]

    @property
    def all_events(self) -> List[Dict]:
        return list(self._entries)

    def __len__(self) -> int:
        return len(self.violations)

    def __repr__(self) -> str:
        return f"ViolationLog({len(self.violations)} violations, {len(self._entries)} total checks)"


class _ConstraintDef:
    """Internal: a registered constraint."""

    def __init__(
        self,
        name: str,
        fn: Callable,
        tools: Optional[List[str]],
        raises: bool,
        message: Optional[str],
    ):
        self.name = name
        self.fn = fn
        self.tools = tools  # None = applies to all tools
        self.raises = raises
        self.message = message

    def applies_to(self, tool: str) -> bool:
        return self.tools is None or tool in self.tools

    def check(self, tool: str, args: Dict) -> Tuple[bool, str]:
        """
        Check the constraint. Returns (passes, reason).
        passes=True means the tool call is ALLOWED.
        """
        sig = inspect.signature(self.fn)
        params = list(sig.parameters.keys())

        if len(params) == 0:
            result = self.fn()
        elif len(params) == 1:
            result = self.fn(args)
        else:
            result = self.fn(tool, args)

        if isinstance(result, tuple):
            passes, reason = result[0], str(result[1]) if len(result) > 1 else ""
        elif isinstance(result, bool):
            passes = result
            reason = self.message or (f"Constraint '{self.name}' violated" if not passes else "")
        elif result is None:
            passes = True
            reason = ""
        else:
            passes = bool(result)
            reason = self.message or (f"Constraint '{self.name}' violated" if not passes else "")

        return passes, reason


class ConstraintEnforcer:
    """
    Enforce rules on tool calls at the Python level.

    Unlike prompt-based constraints, these rules live in your code — the
    agent cannot see or modify them. When a tool call violates a constraint,
    a ConstraintViolation is raised before the tool executes.

    Usage::

        enforcer = ConstraintEnforcer()

        @enforcer.add
        def no_shell_deletion(tool: str, args: dict) -> bool:
            if tool == "bash":
                return "rm -rf" not in args.get("command", "")
            return True

        # Wrap individual tool functions
        @enforcer.protect("bash")
        def run_bash(command: str) -> str:
            return subprocess.run(command, shell=True).stdout

        # Or wrap a dict of tools
        tools = enforcer.protect_all({
            "bash": lambda args: run_bash(**args),
            "read_file": lambda args: open(args["path"]).read(),
        })

    All constraint checks happen BEFORE the tool executes.
    If a constraint raises=False (log-only mode), violations are logged
    but the call proceeds.
    """

    def __init__(self, raises: bool = True):
        """
        Args:
            raises: Default behavior when a constraint is violated.
                    True (default) = raise ConstraintViolation and block the call.
                    False = log the violation but allow the call to proceed.
        """
        self._constraints: List[_ConstraintDef] = []
        self._default_raises = raises
        self.log = ViolationLog()

    # ------------------------------------------------------------------
    # Constraint registration
    # ------------------------------------------------------------------

    def add(
        self,
        fn: Optional[Callable] = None,
        *,
        name: Optional[str] = None,
        tools: Optional[List[str]] = None,
        raises: Optional[bool] = None,
        message: Optional[str] = None,
    ) -> Any:
        """
        Register a constraint function.

        The function signature can be:
        - fn(tool: str, args: dict) -> bool
        - fn(args: dict) -> bool
        - fn() -> bool

        Returns True to ALLOW the call, False or raises to BLOCK it.

        Can be used as a decorator:
            @enforcer.add
            def no_deletion(tool, args): ...

        Or with options:
            @enforcer.add(tools=["bash"], message="No deletions allowed")
            def no_deletion(tool, args): ...
        """
        if fn is None:
            # Called with arguments: @enforcer.add(tools=["bash"])
            def decorator(func: Callable) -> Callable:
                self._register(func, name=name, tools=tools, raises=raises, message=message)
                return func
            return decorator
        else:
            # Called without arguments: @enforcer.add or enforcer.add(fn)
            self._register(fn, name=name, tools=tools, raises=raises, message=message)
            return fn

    def _register(
        self,
        fn: Callable,
        name: Optional[str],
        tools: Optional[List[str]],
        raises: Optional[bool],
        message: Optional[str],
    ) -> None:
        cdef = _ConstraintDef(
            name=name or fn.__name__,
            fn=fn,
            tools=tools,
            raises=raises if raises is not None else self._default_raises,
            message=message,
        )
        self._constraints.append(cdef)

    def remove(self, name: str) -> bool:
        """Remove a constraint by name. Returns True if found."""
        before = len(self._constraints)
        self._constraints = [c for c in self._constraints if c.name != name]
        return len(self._constraints) < before

    def clear(self) -> None:
        """Remove all constraints."""
        self._constraints.clear()

    # ------------------------------------------------------------------
    # Enforcement
    # ------------------------------------------------------------------

    def check(self, tool: str, args: Dict) -> None:
        """
        Run all applicable constraints for a tool call.
        Raises ConstraintViolation if any constraint fails (and raises=True).
        Always logs violations.
        """
        for constraint in self._constraints:
            if not constraint.applies_to(tool):
                continue
            try:
                passes, reason = constraint.check(tool, args)
            except ConstraintViolation as cv:
                self.log.record(constraint.name, tool, args, passed=False, blocked=True)
                raise cv
            except Exception as e:
                # Constraint function itself raised an error — treat as violation
                passes = False
                reason = f"Constraint check error: {e}"

            if not passes:
                self.log.record(
                    constraint.name, tool, args,
                    passed=False,
                    blocked=constraint.raises,
                )
                if constraint.raises:
                    raise ConstraintViolation(
                        constraint_name=constraint.name,
                        tool=tool,
                        tool_args=args,
                        message=reason or constraint.message or (
                            f"Constraint '{constraint.name}' violated by tool '{tool}'"
                        ),
                    )
            else:
                self.log.record(constraint.name, tool, args, passed=True, blocked=False)

    def protect(self, tool_name: str) -> Callable:
        """
        Decorator that wraps a tool function with constraint enforcement.

            @enforcer.protect("bash")
            def run_bash(command: str) -> str:
                return subprocess.run(command, shell=True).stdout
        """
        def decorator(fn: Callable) -> Callable:
            @functools.wraps(fn)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Build an args dict for constraint checking
                sig = inspect.signature(fn)
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                self.check(tool_name, dict(bound.arguments))
                return fn(*args, **kwargs)
            wrapper._constraint_enforcer = self
            wrapper._tool_name = tool_name
            return wrapper
        return decorator

    def protect_fn(self, tool_name: str, fn: Callable) -> Callable:
        """
        Wrap a callable with constraint enforcement for tool_name.

            checked_bash = enforcer.protect_fn("bash", run_bash)
        """
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            sig = inspect.signature(fn)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            self.check(tool_name, dict(bound.arguments))
            return fn(*args, **kwargs)
        wrapper._constraint_enforcer = self
        wrapper._tool_name = tool_name
        return wrapper

    def protect_all(self, tools: Dict[str, Callable]) -> Dict[str, Callable]:
        """
        Wrap a dict of {tool_name: callable} with constraint enforcement.

            tools = enforcer.protect_all({
                "bash": lambda args: run_bash(**args),
                "read_file": lambda args: open(args["path"]).read(),
            })
        """
        return {
            name: self._wrap_dict_tool(name, fn)
            for name, fn in tools.items()
        }

    def _wrap_dict_tool(self, tool_name: str, fn: Callable) -> Callable:
        """Wrap a dict-style tool function (takes a single dict arg)."""
        @functools.wraps(fn)
        def wrapper(args: Dict) -> Any:
            self.check(tool_name, args)
            return fn(args)
        wrapper._constraint_enforcer = self
        wrapper._tool_name = tool_name
        return wrapper

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def constraint_names(self) -> List[str]:
        return [c.name for c in self._constraints]

    def __len__(self) -> int:
        return len(self._constraints)

    def __repr__(self) -> str:
        return (
            f"ConstraintEnforcer("
            f"constraints={len(self._constraints)}, "
            f"violations={len(self.log)}, "
            f"raises={self._default_raises})"
        )
