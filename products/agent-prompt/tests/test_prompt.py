"""
Tests for agent-prompt.
"""

import time
import unittest

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_prompt import (
    PromptTemplate,
    ChatTemplate,
    Message,
    PromptVersion,
    estimate_tokens,
)
from agent_prompt.estimate import estimate_messages_tokens


# ---------------------------------------------------------------------------
# PromptTemplate tests

class TestPromptTemplate(unittest.TestCase):

    def test_simple_render(self):
        t = PromptTemplate("Hello, {name}!")
        self.assertEqual(t.render(name="world"), "Hello, world!")

    def test_multiple_variables(self):
        t = PromptTemplate("You are a {role}. Respond to: {query}")
        result = t.render(role="expert", query="What is Python?")
        self.assertIn("expert", result)
        self.assertIn("What is Python?", result)

    def test_missing_variable_raises_key_error(self):
        t = PromptTemplate("Hello, {name}!")
        with self.assertRaises(KeyError):
            t.render()

    def test_extra_variables_are_ignored(self):
        # Extra kwargs not in template are silently ignored
        t = PromptTemplate("Hello, {name}!")
        result = t.render(name="Alice", extra="unused")
        self.assertEqual(result, "Hello, Alice!")

    def test_no_variables(self):
        t = PromptTemplate("Static prompt")
        self.assertEqual(t.render(), "Static prompt")

    def test_variables_property(self):
        t = PromptTemplate("{a} and {b} and {a}")
        self.assertEqual(t.variables, ["a", "b"])  # sorted, deduplicated

    def test_variables_empty(self):
        t = PromptTemplate("No variables here")
        self.assertEqual(t.variables, [])

    def test_escaped_braces(self):
        t = PromptTemplate("Use {{literal}} braces and {value}")
        result = t.render(value="dynamic")
        self.assertEqual(result, "Use {literal} braces and dynamic")

    def test_render_converts_to_string(self):
        t = PromptTemplate("Count: {n}")
        self.assertEqual(t.render(n=42), "Count: 42")

    def test_to_message(self):
        t = PromptTemplate("Hello, {name}!")
        msg = t.to_message("user", name="Alice")
        self.assertEqual(msg["role"], "user")
        self.assertEqual(msg["content"], "Hello, Alice!")

    def test_to_message_system(self):
        t = PromptTemplate("You are a {role}.")
        msg = t.to_message("system", role="helpful assistant")
        self.assertEqual(msg["role"], "system")

    def test_equality(self):
        a = PromptTemplate("Hello {name}")
        b = PromptTemplate("Hello {name}")
        c = PromptTemplate("Goodbye {name}")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_repr_contains_preview(self):
        t = PromptTemplate("Hello {name}!")
        r = repr(t)
        self.assertIn("Hello", r)
        self.assertIn("name", r)

    def test_repr_truncates_long_template(self):
        t = PromptTemplate("x" * 100)
        r = repr(t)
        self.assertIn("...", r)

    def test_add_concatenates(self):
        a = PromptTemplate("Hello {name}. ")
        b = PromptTemplate("You are a {role}.")
        c = a + b
        result = c.render(name="Alice", role="expert")
        self.assertEqual(result, "Hello Alice. You are a expert.")

    def test_add_variables_union(self):
        a = PromptTemplate("{x}")
        b = PromptTemplate("{y}")
        c = a + b
        self.assertEqual(c.variables, ["x", "y"])

    def test_estimate_tokens_returns_positive(self):
        t = PromptTemplate("You are a helpful assistant.")
        n = t.estimate_tokens()
        self.assertGreater(n, 0)

    def test_estimate_tokens_longer_is_more(self):
        short = PromptTemplate("Hello")
        long = PromptTemplate("This is a much longer prompt with many more words and tokens.")
        self.assertGreater(long.estimate_tokens(), short.estimate_tokens())


# ---------------------------------------------------------------------------
# PromptTemplate.partial tests

class TestPromptTemplatePartial(unittest.TestCase):

    def test_partial_fills_some_variables(self):
        t = PromptTemplate("Hello {name}, you are {role}.")
        filled = t.partial(name="Alice")
        # {name} is filled, {role} still a placeholder
        result = filled.render(role="expert")
        self.assertEqual(result, "Hello Alice, you are expert.")

    def test_partial_returns_new_template(self):
        t = PromptTemplate("{a} and {b}")
        p = t.partial(a="x")
        self.assertIsNot(t, p)

    def test_partial_chaining(self):
        t = PromptTemplate("{a} {b} {c}")
        p = t.partial(a="1").partial(b="2")
        result = p.render(c="3")
        self.assertEqual(result, "1 2 3")

    def test_partial_all_variables(self):
        t = PromptTemplate("Hello {name}!")
        p = t.partial(name="World")
        result = p.render()
        self.assertEqual(result, "Hello World!")

    def test_partial_does_not_modify_original(self):
        t = PromptTemplate("{a} {b}")
        t.partial(a="x")
        # Original still requires both variables
        self.assertIn("a", t.variables)
        self.assertIn("b", t.variables)


# ---------------------------------------------------------------------------
# Message tests

class TestMessage(unittest.TestCase):

    def test_basic_message(self):
        msg = Message(role="user", content="Hello")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "Hello")

    def test_to_dict(self):
        msg = Message(role="system", content="You are helpful.")
        d = msg.to_dict()
        self.assertEqual(d["role"], "system")
        self.assertEqual(d["content"], "You are helpful.")

    def test_from_template(self):
        tmpl = PromptTemplate("Hi, {name}!")
        msg = Message.from_template("user", tmpl, name="Alice")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "Hi, Alice!")

    def test_estimate_tokens(self):
        msg = Message(role="user", content="This is a test message for token estimation.")
        n = msg.estimate_tokens()
        self.assertGreater(n, 0)


# ---------------------------------------------------------------------------
# ChatTemplate tests

class TestChatTemplate(unittest.TestCase):

    def _make_chat(self):
        return ChatTemplate(
            system=PromptTemplate("You are a {role} assistant."),
            turns=[
                ("user", PromptTemplate("What is {concept}?")),
                ("assistant", PromptTemplate("{concept} is important.")),
            ],
        )

    def test_render_returns_list(self):
        chat = self._make_chat()
        msgs = chat.render(role="helpful", concept="entropy")
        self.assertIsInstance(msgs, list)

    def test_render_system_first(self):
        chat = self._make_chat()
        msgs = chat.render(role="helpful", concept="entropy")
        self.assertEqual(msgs[0]["role"], "system")
        self.assertIn("helpful", msgs[0]["content"])

    def test_render_turns(self):
        chat = self._make_chat()
        msgs = chat.render(role="helpful", concept="entropy")
        self.assertEqual(len(msgs), 3)
        self.assertEqual(msgs[1]["role"], "user")
        self.assertEqual(msgs[2]["role"], "assistant")

    def test_render_variables_substituted(self):
        chat = self._make_chat()
        msgs = chat.render(role="Python", concept="decorators")
        self.assertIn("Python", msgs[0]["content"])
        self.assertIn("decorators", msgs[1]["content"])
        self.assertIn("decorators", msgs[2]["content"])

    def test_render_turns_no_system(self):
        chat = self._make_chat()
        msgs = chat.render_turns(role="helpful", concept="entropy")
        self.assertEqual(len(msgs), 2)
        self.assertEqual(msgs[0]["role"], "user")

    def test_render_missing_variable_raises(self):
        chat = self._make_chat()
        with self.assertRaises(KeyError):
            chat.render(role="helpful")  # missing 'concept'

    def test_variables_from_all_turns(self):
        chat = self._make_chat()
        self.assertIn("role", chat.variables)
        self.assertIn("concept", chat.variables)

    def test_variables_sorted(self):
        chat = ChatTemplate(
            system=PromptTemplate("{z} prompt"),
            turns=[
                ("user", PromptTemplate("{a} question")),
            ],
        )
        self.assertEqual(chat.variables, ["a", "z"])

    def test_no_system(self):
        chat = ChatTemplate(turns=[
            ("user", PromptTemplate("Hello {name}")),
        ])
        msgs = chat.render(name="Alice")
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["role"], "user")

    def test_add_turn(self):
        chat = ChatTemplate()
        chat.add_turn("user", PromptTemplate("Hello {name}"))
        chat.add_turn("assistant", PromptTemplate("Hi there!"))
        msgs = chat.render(name="Bob")
        self.assertEqual(len(msgs), 2)

    def test_add_turn_returns_self(self):
        chat = ChatTemplate()
        result = chat.add_turn("user", PromptTemplate("Hi"))
        self.assertIs(result, chat)

    def test_repr(self):
        chat = self._make_chat()
        r = repr(chat)
        self.assertIn("system=True", r)
        self.assertIn("turns=2", r)

    def test_estimate_tokens(self):
        chat = self._make_chat()
        n = chat.estimate_tokens(role="helpful", concept="entropy")
        self.assertGreater(n, 0)

    def test_partial(self):
        chat = self._make_chat()
        partial_chat = chat.partial(role="Python")
        # 'role' is filled, 'concept' still needed
        msgs = partial_chat.render(concept="generators")
        self.assertIn("Python", msgs[0]["content"])
        self.assertIn("generators", msgs[1]["content"])

    def test_partial_creates_new_chat(self):
        chat = self._make_chat()
        partial_chat = chat.partial(role="Python")
        self.assertIsNot(chat, partial_chat)

    def test_empty_chat(self):
        chat = ChatTemplate()
        msgs = chat.render()
        self.assertEqual(msgs, [])


# ---------------------------------------------------------------------------
# PromptVersion tests

class TestPromptVersion(unittest.TestCase):

    def test_basic_version(self):
        tmpl = PromptTemplate("Hello {name}!")
        v = PromptVersion(tmpl, label="v1.0")
        self.assertEqual(v.label, "v1.0")
        self.assertIsNotNone(v.hash)

    def test_hash_is_12_chars(self):
        v = PromptVersion(PromptTemplate("test"))
        self.assertEqual(len(v.hash), 12)

    def test_same_content_same_hash(self):
        a = PromptVersion(PromptTemplate("Hello {name}!"))
        b = PromptVersion(PromptTemplate("Hello {name}!"))
        self.assertEqual(a.hash, b.hash)

    def test_different_content_different_hash(self):
        a = PromptVersion(PromptTemplate("Hello {name}!"))
        b = PromptVersion(PromptTemplate("Goodbye {name}!"))
        self.assertNotEqual(a.hash, b.hash)

    def test_equality(self):
        a = PromptVersion(PromptTemplate("Hello {name}!"))
        b = PromptVersion(PromptTemplate("Hello {name}!"), label="different label")
        self.assertEqual(a, b)  # equality is hash-based, label-independent

    def test_inequality(self):
        a = PromptVersion(PromptTemplate("Hello"))
        b = PromptVersion(PromptTemplate("World"))
        self.assertNotEqual(a, b)

    def test_render_delegates(self):
        v = PromptVersion(PromptTemplate("Hi, {name}!"), label="v1")
        self.assertEqual(v.render(name="Alice"), "Hi, Alice!")

    def test_to_message_delegates(self):
        v = PromptVersion(PromptTemplate("You are a {role}."), label="v1")
        msg = v.to_message("system", role="assistant")
        self.assertEqual(msg["role"], "system")
        self.assertIn("assistant", msg["content"])

    def test_to_message_raises_for_chat_template(self):
        v = PromptVersion(ChatTemplate(system=PromptTemplate("Hi")))
        with self.assertRaises(TypeError):
            v.to_message("user")

    def test_metadata(self):
        v = PromptVersion(PromptTemplate("test"), metadata={"author": "eng", "version": 1})
        self.assertEqual(v.metadata["author"], "eng")

    def test_created_at(self):
        before = time.time()
        v = PromptVersion(PromptTemplate("test"))
        after = time.time()
        self.assertGreaterEqual(v.created_at, before)
        self.assertLessEqual(v.created_at, after)

    def test_chat_template_version(self):
        chat = ChatTemplate(
            system=PromptTemplate("You are {role}."),
            turns=[("user", PromptTemplate("Hello"))],
        )
        v = PromptVersion(chat, label="v2.0")
        self.assertEqual(len(v.hash), 12)

    def test_repr(self):
        v = PromptVersion(PromptTemplate("test"), label="v1.0")
        r = repr(v)
        self.assertIn("hash=", r)
        self.assertIn("v1.0", r)


# ---------------------------------------------------------------------------
# estimate_tokens tests

class TestEstimateTokens(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(estimate_tokens(""), 0)

    def test_single_word(self):
        n = estimate_tokens("hello")
        self.assertGreater(n, 0)

    def test_longer_text_more_tokens(self):
        short = estimate_tokens("Hello")
        long = estimate_tokens("This is a much longer sentence with many words.")
        self.assertGreater(long, short)

    def test_typical_prompt(self):
        text = "You are a helpful assistant. Please answer the user's question clearly and concisely."
        n = estimate_tokens(text)
        # This is ~15-20 tokens. Estimate should be in 10-35 range.
        self.assertGreater(n, 5)
        self.assertLess(n, 50)

    def test_whitespace_only(self):
        n = estimate_tokens("   ")
        self.assertEqual(n, 0)

    def test_estimate_messages(self):
        msgs = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "What is Python?"},
        ]
        n = estimate_messages_tokens(msgs)
        self.assertGreater(n, 0)

    def test_estimate_messages_empty(self):
        self.assertEqual(estimate_messages_tokens([]), 0)

    def test_estimate_messages_per_message_overhead(self):
        one_msg = [{"role": "user", "content": "hello"}]
        two_msgs = [
            {"role": "user", "content": "hello"},
            {"role": "user", "content": "hello"},
        ]
        # Two messages should cost more due to per-message overhead
        self.assertGreater(estimate_messages_tokens(two_msgs), estimate_messages_tokens(one_msg))


# ---------------------------------------------------------------------------
# Integration tests

class TestIntegration(unittest.TestCase):

    def test_full_chat_workflow(self):
        """Build a complete chat, render, estimate tokens."""
        system = PromptTemplate(
            "You are a {expertise} expert. Always be {style}."
        )
        user_turn = PromptTemplate("Explain {topic} in simple terms.")

        chat = ChatTemplate(
            system=system,
            turns=[("user", user_turn)],
        )

        msgs = chat.render(
            expertise="Python",
            style="concise",
            topic="decorators",
        )

        self.assertEqual(len(msgs), 2)
        self.assertIn("Python", msgs[0]["content"])
        self.assertIn("decorators", msgs[1]["content"])

        token_count = chat.estimate_tokens(
            expertise="Python",
            style="concise",
            topic="decorators",
        )
        self.assertGreater(token_count, 0)

    def test_versioned_ab_test(self):
        """Simulate A/B testing two prompt versions."""
        v1 = PromptVersion(
            PromptTemplate("Answer briefly: {question}"),
            label="brief",
        )
        v2 = PromptVersion(
            PromptTemplate("Answer step-by-step: {question}"),
            label="detailed",
        )

        self.assertNotEqual(v1.hash, v2.hash)

        msg_v1 = v1.to_message("user", question="What is entropy?")
        msg_v2 = v2.to_message("user", question="What is entropy?")

        self.assertIn("briefly", msg_v1["content"])
        self.assertIn("step-by-step", msg_v2["content"])

    def test_partial_then_version(self):
        """Partially fill a template, then wrap in a version."""
        base = PromptTemplate("You are a {role}. Respond to: {query}")
        for_support = base.partial(role="support agent")
        v = PromptVersion(for_support, label="support-v1")

        result = v.render(query="My order is late.")
        self.assertIn("support agent", result)
        self.assertIn("My order is late.", result)

    def test_message_list_to_anthropic_format(self):
        """Rendered messages should be directly usable with Anthropic API."""
        system = PromptTemplate("You are {role}.")
        chat = ChatTemplate(
            system=system,
            turns=[("user", PromptTemplate("Hello {name}"))],
        )

        msgs = chat.render(role="helpful", name="Alice")

        # Simulate Anthropic API call format
        system_content = msgs[0]["content"]
        user_messages = [m for m in msgs[1:] if m["role"] in ("user", "assistant")]

        self.assertIn("helpful", system_content)
        self.assertEqual(len(user_messages), 1)
        self.assertIn("Alice", user_messages[0]["content"])


if __name__ == "__main__":
    unittest.main()
