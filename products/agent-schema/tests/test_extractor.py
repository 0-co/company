"""Tests for JSONExtractor."""

import unittest

from agent_schema import JSONExtractor


class TestJSONExtractor(unittest.TestCase):

    def setUp(self):
        self.e = JSONExtractor()

    # ------------------------------------------------------------------
    # Direct JSON
    # ------------------------------------------------------------------

    def test_direct_json_object(self):
        text = '{"key": "value", "n": 42}'
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        import json
        parsed = json.loads(raw)
        self.assertEqual(parsed["key"], "value")

    def test_direct_json_array(self):
        text = '[1, 2, 3]'
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        import json
        self.assertEqual(json.loads(raw), [1, 2, 3])

    def test_direct_json_whitespace_stripped(self):
        text = '   {"a": 1}   '
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)

    # ------------------------------------------------------------------
    # Fenced code blocks
    # ------------------------------------------------------------------

    def test_json_in_backtick_json_block(self):
        text = '```json\n{"name": "Alice", "score": 90}\n```'
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        import json
        parsed = json.loads(raw)
        self.assertEqual(parsed["name"], "Alice")

    def test_json_in_plain_backtick_block(self):
        text = '```\n{"x": true}\n```'
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        import json
        self.assertTrue(json.loads(raw)["x"])

    def test_json_in_backtick_block_with_surrounding_text(self):
        text = "Sure, here you go:\n```json\n{\"a\": 1}\n```\nHope that helps!"
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        import json
        self.assertEqual(json.loads(raw)["a"], 1)

    def test_json_in_backtick_block_uppercase_tag(self):
        text = "```JSON\n{\"b\": 2}\n```"
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)

    # ------------------------------------------------------------------
    # JSON embedded in surrounding text (no code block)
    # ------------------------------------------------------------------

    def test_json_with_surrounding_text(self):
        text = 'Here is the JSON: {"result": "ok", "code": 200} end of message.'
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        import json
        parsed = json.loads(raw)
        self.assertEqual(parsed["result"], "ok")

    def test_json_after_explanation(self):
        text = "The structured output is as follows:\n\n{\"items\": [1,2,3], \"total\": 3}"
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)

    # ------------------------------------------------------------------
    # Deeply nested structures
    # ------------------------------------------------------------------

    def test_deeply_nested_braces(self):
        obj = {"a": {"b": {"c": {"d": 4}}}}
        import json
        text = "result: " + json.dumps(obj)
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        self.assertEqual(json.loads(raw), obj)

    def test_nested_array_in_object(self):
        import json
        obj = {"tags": ["x", "y"], "nested": [{"id": 1}, {"id": 2}]}
        text = json.dumps(obj)
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        self.assertEqual(json.loads(raw), obj)

    def test_json_with_string_containing_braces(self):
        """Braces inside string literals should not confuse the parser."""
        import json
        obj = {"code": "if x { return 1 }", "ok": True}
        text = json.dumps(obj)
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        parsed = json.loads(raw)
        self.assertEqual(parsed["code"], "if x { return 1 }")

    # ------------------------------------------------------------------
    # No JSON
    # ------------------------------------------------------------------

    def test_no_json_returns_none(self):
        text = "This is plain text with no JSON at all."
        self.assertIsNone(self.e.extract(text))

    def test_empty_string_returns_none(self):
        self.assertIsNone(self.e.extract(""))

    def test_only_partial_json_returns_none(self):
        self.assertIsNone(self.e.extract("{unclosed"))

    # ------------------------------------------------------------------
    # extract_and_parse
    # ------------------------------------------------------------------

    def test_extract_and_parse_happy_path(self):
        text = '{"greeting": "hello"}'
        parsed = self.e.extract_and_parse(text)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["greeting"], "hello")

    def test_extract_and_parse_markdown_input(self):
        text = "```json\n{\"x\": 99}\n```"
        parsed = self.e.extract_and_parse(text)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["x"], 99)

    def test_extract_and_parse_returns_list(self):
        text = "[1, 2, 3]"
        parsed = self.e.extract_and_parse(text)
        self.assertEqual(parsed, [1, 2, 3])

    def test_extract_and_parse_none_input(self):
        result = self.e.extract_and_parse(None)
        self.assertIsNone(result)

    def test_extract_and_parse_no_json(self):
        result = self.e.extract_and_parse("no json here")
        self.assertIsNone(result)

    # ------------------------------------------------------------------
    # Edge cases
    # ------------------------------------------------------------------

    def test_array_with_surrounding_text(self):
        text = "The list is: [\"a\", \"b\", \"c\"]."
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        import json
        self.assertEqual(json.loads(raw), ["a", "b", "c"])

    def test_multiple_code_blocks_picks_first_valid(self):
        text = "```json\n{\"first\": 1}\n```\n```json\n{\"second\": 2}\n```"
        raw = self.e.extract(text)
        self.assertIsNotNone(raw)
        import json
        parsed = json.loads(raw)
        self.assertEqual(parsed["first"], 1)

    def test_json_with_unicode(self):
        import json
        obj = {"msg": "caf\u00e9", "n": 1}
        text = json.dumps(obj)
        parsed = self.e.extract_and_parse(text)
        self.assertIsNotNone(parsed)
        self.assertIn("caf", parsed["msg"])


if __name__ == "__main__":
    unittest.main()
