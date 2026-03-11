"""Tests for SchemaValidator."""

import unittest

from agent_schema import SchemaValidator, ValidationResult


SIMPLE_SCHEMA = {
    "type": "object",
    "required": ["name", "score"],
    "properties": {
        "name": {"type": "string"},
        "score": {"type": "number", "minimum": 0, "maximum": 100},
        "tags": {"type": "array", "items": {"type": "string"}},
        "metadata": {"type": "object"},
        "active": {"type": "boolean"},
        "status": {"type": "string", "enum": ["pending", "done", "failed"]},
    },
}


class TestValidatorBasic(unittest.TestCase):

    def setUp(self):
        self.v = SchemaValidator()

    # ------------------------------------------------------------------
    # Happy path
    # ------------------------------------------------------------------

    def test_valid_full_object(self):
        data = {
            "name": "Alice",
            "score": 95.0,
            "tags": ["python", "ai"],
            "metadata": {"key": "value"},
            "active": True,
            "status": "done",
        }
        result = self.v.validate(data, SIMPLE_SCHEMA)
        self.assertTrue(result.valid)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.data, data)

    def test_valid_minimal_object(self):
        """Only required fields present — still valid."""
        result = self.v.validate({"name": "Bob", "score": 42}, SIMPLE_SCHEMA)
        self.assertTrue(result.valid)

    def test_valid_score_boundary_min(self):
        result = self.v.validate({"name": "x", "score": 0}, SIMPLE_SCHEMA)
        self.assertTrue(result.valid)

    def test_valid_score_boundary_max(self):
        result = self.v.validate({"name": "x", "score": 100}, SIMPLE_SCHEMA)
        self.assertTrue(result.valid)

    # ------------------------------------------------------------------
    # Missing required fields
    # ------------------------------------------------------------------

    def test_missing_required_field_name(self):
        result = self.v.validate({"score": 10}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(any("name" in e for e in result.errors))
        self.assertIsNone(result.data)

    def test_missing_required_field_score(self):
        result = self.v.validate({"name": "Alice"}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(any("score" in e for e in result.errors))

    def test_missing_both_required_fields(self):
        result = self.v.validate({}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertEqual(len([e for e in result.errors if "required" in e.lower() or "missing" in e.lower()]), 2)

    # ------------------------------------------------------------------
    # Wrong types
    # ------------------------------------------------------------------

    def test_wrong_type_string_for_number(self):
        result = self.v.validate({"name": "x", "score": "high"}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(any("score" in e for e in result.errors))

    def test_wrong_type_number_for_string(self):
        result = self.v.validate({"name": 123, "score": 10}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(any("name" in e for e in result.errors))

    def test_wrong_type_bool_not_number(self):
        """True is a bool, not a number — should fail number type check."""
        result = self.v.validate({"name": "x", "score": True}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)

    def test_wrong_type_bool_not_integer(self):
        schema = {"type": "object", "properties": {"n": {"type": "integer"}}}
        result = self.v.validate({"n": True}, schema)
        self.assertFalse(result.valid)

    def test_wrong_type_dict_for_array(self):
        result = self.v.validate({"name": "x", "score": 1, "tags": {"a": 1}}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)

    def test_wrong_type_list_for_object(self):
        result = self.v.validate({"name": "x", "score": 1, "metadata": [1, 2]}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)

    def test_wrong_type_string_for_boolean(self):
        result = self.v.validate({"name": "x", "score": 1, "active": "yes"}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)

    # ------------------------------------------------------------------
    # Enum
    # ------------------------------------------------------------------

    def test_enum_valid_value(self):
        result = self.v.validate({"name": "x", "score": 1, "status": "pending"}, SIMPLE_SCHEMA)
        self.assertTrue(result.valid)

    def test_enum_invalid_value(self):
        result = self.v.validate({"name": "x", "score": 1, "status": "unknown"}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(any("enum" in e for e in result.errors))

    # ------------------------------------------------------------------
    # Number constraints
    # ------------------------------------------------------------------

    def test_number_below_minimum(self):
        result = self.v.validate({"name": "x", "score": -1}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(any("minimum" in e for e in result.errors))

    def test_number_above_maximum(self):
        result = self.v.validate({"name": "x", "score": 101}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(any("maximum" in e for e in result.errors))

    # ------------------------------------------------------------------
    # String constraints
    # ------------------------------------------------------------------

    def test_string_minLength_pass(self):
        schema = {"type": "object", "properties": {"s": {"type": "string", "minLength": 3}}}
        result = self.v.validate({"s": "abc"}, schema)
        self.assertTrue(result.valid)

    def test_string_minLength_fail(self):
        schema = {"type": "object", "properties": {"s": {"type": "string", "minLength": 3}}}
        result = self.v.validate({"s": "ab"}, schema)
        self.assertFalse(result.valid)
        self.assertTrue(any("minLength" in e for e in result.errors))

    def test_string_maxLength_pass(self):
        schema = {"type": "object", "properties": {"s": {"type": "string", "maxLength": 5}}}
        result = self.v.validate({"s": "hello"}, schema)
        self.assertTrue(result.valid)

    def test_string_maxLength_fail(self):
        schema = {"type": "object", "properties": {"s": {"type": "string", "maxLength": 5}}}
        result = self.v.validate({"s": "toolong"}, schema)
        self.assertFalse(result.valid)
        self.assertTrue(any("maxLength" in e for e in result.errors))

    # ------------------------------------------------------------------
    # Array item validation
    # ------------------------------------------------------------------

    def test_array_items_valid(self):
        result = self.v.validate({"name": "x", "score": 1, "tags": ["a", "b"]}, SIMPLE_SCHEMA)
        self.assertTrue(result.valid)

    def test_array_items_wrong_type(self):
        result = self.v.validate({"name": "x", "score": 1, "tags": [1, 2, 3]}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        # Should report error on each bad item
        self.assertTrue(len(result.errors) >= 3)

    def test_array_items_mixed(self):
        result = self.v.validate({"name": "x", "score": 1, "tags": ["ok", 99]}, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)

    # ------------------------------------------------------------------
    # Nested objects
    # ------------------------------------------------------------------

    def test_nested_object_valid(self):
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {"id": {"type": "integer"}},
                }
            },
        }
        result = self.v.validate({"user": {"id": 42}}, schema)
        self.assertTrue(result.valid)

    def test_nested_object_missing_required(self):
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {"id": {"type": "integer"}},
                }
            },
        }
        result = self.v.validate({"user": {}}, schema)
        self.assertFalse(result.valid)
        self.assertTrue(any("id" in e for e in result.errors))

    # ------------------------------------------------------------------
    # Null type
    # ------------------------------------------------------------------

    def test_null_type_valid(self):
        schema = {"type": "object", "properties": {"val": {"type": "null"}}}
        result = self.v.validate({"val": None}, schema)
        self.assertTrue(result.valid)

    def test_null_type_wrong(self):
        schema = {"type": "object", "properties": {"val": {"type": "null"}}}
        result = self.v.validate({"val": "not null"}, schema)
        self.assertFalse(result.valid)

    # ------------------------------------------------------------------
    # parse_and_validate
    # ------------------------------------------------------------------

    def test_parse_and_validate_valid_json_string(self):
        text = '{"name": "Alice", "score": 80}'
        result = self.v.parse_and_validate(text, SIMPLE_SCHEMA)
        self.assertTrue(result.valid)
        self.assertEqual(result.data["name"], "Alice")

    def test_parse_and_validate_invalid_json_string(self):
        result = self.v.parse_and_validate("not json at all", SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(len(result.errors) > 0)

    def test_parse_and_validate_json_in_markdown(self):
        text = """Here is the result:
```json
{"name": "Bob", "score": 55}
```
That's all."""
        result = self.v.parse_and_validate(text, SIMPLE_SCHEMA)
        self.assertTrue(result.valid)
        self.assertEqual(result.data["score"], 55)

    def test_parse_and_validate_fails_schema(self):
        text = '{"name": "Alice", "score": 200}'
        result = self.v.parse_and_validate(text, SIMPLE_SCHEMA)
        self.assertFalse(result.valid)
        self.assertTrue(any("maximum" in e for e in result.errors))

    # ------------------------------------------------------------------
    # Integer type
    # ------------------------------------------------------------------

    def test_integer_type_int_passes(self):
        schema = {"type": "object", "properties": {"n": {"type": "integer"}}}
        result = self.v.validate({"n": 5}, schema)
        self.assertTrue(result.valid)

    def test_integer_type_float_fails(self):
        schema = {"type": "object", "properties": {"n": {"type": "integer"}}}
        result = self.v.validate({"n": 5.5}, schema)
        self.assertFalse(result.valid)


if __name__ == "__main__":
    unittest.main()
