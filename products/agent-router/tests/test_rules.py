import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_router.rules import (
    input_tokens_under, input_tokens_over,
    last_message_under, last_message_over,
    message_count_under, message_count_over,
    contains_keyword, custom, always,
)


def msg(content):
    return {"role": "user", "content": content}


class TestInputTokensUnder(unittest.TestCase):
    def test_short_text_passes(self):
        # 40 chars / 4 = 10 estimated tokens — under 50
        condition = input_tokens_under(50)
        messages = [msg("Hello world this is a test message.")]
        self.assertTrue(condition(messages))

    def test_long_text_fails(self):
        # 2000 chars / 4 = 500 estimated tokens — not under 50
        condition = input_tokens_under(50)
        messages = [msg("x" * 2000)]
        self.assertFalse(condition(messages))

    def test_exactly_at_boundary_fails(self):
        # exactly n tokens estimated -> not under n
        condition = input_tokens_under(100)
        messages = [msg("x" * 400)]  # 400 / 4 = 100, not < 100
        self.assertFalse(condition(messages))

    def test_just_under_boundary_passes(self):
        condition = input_tokens_under(100)
        messages = [msg("x" * 396)]  # 396 / 4 = 99.0 < 100
        self.assertTrue(condition(messages))


class TestInputTokensOver(unittest.TestCase):
    def test_long_text_passes(self):
        condition = input_tokens_over(50)
        messages = [msg("x" * 2000)]  # 500 estimated tokens >= 50
        self.assertTrue(condition(messages))

    def test_short_text_fails(self):
        condition = input_tokens_over(500)
        messages = [msg("hi")]  # tiny
        self.assertFalse(condition(messages))

    def test_exactly_at_boundary_passes(self):
        condition = input_tokens_over(100)
        messages = [msg("x" * 400)]  # 400 / 4 = 100 >= 100
        self.assertTrue(condition(messages))


class TestLastMessageUnder(unittest.TestCase):
    def test_short_last_message_passes(self):
        condition = last_message_under(100)
        messages = [msg("short")]
        self.assertTrue(condition(messages))

    def test_long_last_message_fails(self):
        condition = last_message_under(100)
        messages = [msg("x" * 200)]
        self.assertFalse(condition(messages))

    def test_empty_messages_passes(self):
        condition = last_message_under(100)
        self.assertTrue(condition([]))

    def test_uses_last_message_not_first(self):
        condition = last_message_under(10)
        messages = [
            msg("this is a longer first message"),
            msg("short"),
        ]
        self.assertTrue(condition(messages))


class TestLastMessageOver(unittest.TestCase):
    def test_long_last_message_passes(self):
        condition = last_message_over(10)
        messages = [msg("this is a longer message than 10 chars")]
        self.assertTrue(condition(messages))

    def test_short_last_message_fails(self):
        condition = last_message_over(100)
        messages = [msg("hi")]
        self.assertFalse(condition(messages))

    def test_empty_messages_fails(self):
        condition = last_message_over(0)
        self.assertFalse(condition([]))


class TestMessageCountUnder(unittest.TestCase):
    def test_few_messages_pass(self):
        condition = message_count_under(5)
        messages = [msg("a"), msg("b")]
        self.assertTrue(condition(messages))

    def test_many_messages_fail(self):
        condition = message_count_under(3)
        messages = [msg("a"), msg("b"), msg("c"), msg("d")]
        self.assertFalse(condition(messages))

    def test_exactly_at_boundary_fails(self):
        condition = message_count_under(3)
        messages = [msg("a"), msg("b"), msg("c")]
        self.assertFalse(condition(messages))

    def test_empty_messages_pass(self):
        condition = message_count_under(1)
        self.assertTrue(condition([]))


class TestMessageCountOver(unittest.TestCase):
    def test_many_messages_pass(self):
        condition = message_count_over(3)
        messages = [msg("a"), msg("b"), msg("c"), msg("d")]
        self.assertTrue(condition(messages))

    def test_few_messages_fail(self):
        condition = message_count_over(5)
        messages = [msg("a"), msg("b")]
        self.assertFalse(condition(messages))

    def test_exactly_at_boundary_passes(self):
        condition = message_count_over(3)
        messages = [msg("a"), msg("b"), msg("c")]
        self.assertTrue(condition(messages))


class TestContainsKeyword(unittest.TestCase):
    def test_keyword_present_passes(self):
        condition = contains_keyword("urgent")
        messages = [msg("This is urgent please help")]
        self.assertTrue(condition(messages))

    def test_keyword_absent_fails(self):
        condition = contains_keyword("urgent")
        messages = [msg("Just a regular question")]
        self.assertFalse(condition(messages))

    def test_case_insensitive_by_default(self):
        condition = contains_keyword("URGENT")
        messages = [msg("this is urgent")]
        self.assertTrue(condition(messages))

    def test_case_sensitive_respects_case(self):
        condition = contains_keyword("URGENT", case_sensitive=True)
        messages = [msg("this is urgent")]
        self.assertFalse(condition(messages))

    def test_case_sensitive_exact_match_passes(self):
        condition = contains_keyword("URGENT", case_sensitive=True)
        messages = [msg("this is URGENT")]
        self.assertTrue(condition(messages))

    def test_multiple_keywords_any_match(self):
        condition = contains_keyword("urgent", "critical", "important")
        messages = [msg("This is a critical issue")]
        self.assertTrue(condition(messages))

    def test_multiple_keywords_none_match_fails(self):
        condition = contains_keyword("urgent", "critical", "important")
        messages = [msg("This is a normal question")]
        self.assertFalse(condition(messages))

    def test_matches_across_multiple_messages(self):
        condition = contains_keyword("code")
        messages = [
            msg("Can you help me"),
            msg("I need to write some code"),
        ]
        self.assertTrue(condition(messages))

    def test_empty_messages_fails(self):
        condition = contains_keyword("anything")
        self.assertFalse(condition([]))


class TestAlways(unittest.TestCase):
    def test_always_returns_true(self):
        condition = always()
        self.assertTrue(condition([]))
        self.assertTrue(condition([msg("hello")]))
        self.assertTrue(condition([msg("x" * 10000)]))

    def test_always_ignores_context(self):
        condition = always()
        self.assertTrue(condition([], foo="bar", baz=999))


class TestCustom(unittest.TestCase):
    def test_wraps_arbitrary_function(self):
        def my_rule(messages, **context):
            return len(messages) == 1

        condition = custom(my_rule)
        self.assertTrue(condition([msg("only one")]))
        self.assertFalse(condition([msg("one"), msg("two")]))

    def test_custom_receives_context(self):
        received = {}

        def my_rule(messages, **context):
            received.update(context)
            return True

        condition = custom(my_rule)
        condition([], user_id="abc123")
        self.assertEqual(received, {"user_id": "abc123"})


class TestEmptyMessagesHandledGracefully(unittest.TestCase):
    """No IndexError or KeyError on empty message lists."""

    def test_input_tokens_under_empty(self):
        self.assertTrue(input_tokens_under(100)([]))

    def test_input_tokens_over_empty(self):
        self.assertFalse(input_tokens_over(1)([]))

    def test_last_message_under_empty(self):
        self.assertTrue(last_message_under(100)([]))

    def test_last_message_over_empty(self):
        self.assertFalse(last_message_over(0)([]))

    def test_message_count_under_empty(self):
        self.assertTrue(message_count_under(1)([]))

    def test_message_count_over_empty(self):
        self.assertFalse(message_count_over(1)([]))

    def test_contains_keyword_empty(self):
        self.assertFalse(contains_keyword("word")([]))

    def test_always_empty(self):
        self.assertTrue(always()([]))


if __name__ == "__main__":
    unittest.main()
