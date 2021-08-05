import unittest

from carrierpigeon import utils


class UtilsTestCase(unittest.TestCase):
    def test_create_schema_minimal(self):
        fields = [
            ["msg", "string"],
        ]
        schema = utils.create_schema(utils.BASE_SCHEMA, "test", fields)
        self.assertEqual(
            schema,
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "https://example.com/test.json",
                "title": "Test",
                "description": "",
                "type": "object",
                "properties": {"msg": {"type": "string"}},
                "required": [],
                "additionalProperties": False,
            },
        )

    def test_create_schema_required(self):
        fields = [
            ["msg", "string"],
            ["created", "number"],
        ]
        schema = utils.create_schema(utils.BASE_SCHEMA, "test", fields, required=["msg"])
        self.assertEqual(
            schema,
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "https://example.com/test.json",
                "title": "Test",
                "description": "",
                "type": "object",
                "properties": {"msg": {"type": "string"}, "created": {"type": "number"}},
                "required": ["msg"],
                "additionalProperties": False,
            },
        )

    def test_create_schema_version(self):
        fields = [
            ["msg", "string"],
            ["created", "number"],
        ]
        schema = utils.create_schema(utils.BASE_SCHEMA, "test", fields, version=3)
        self.assertEqual(
            schema,
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "https://example.com/test.v3.json",
                "title": "Test",
                "description": "",
                "type": "object",
                "properties": {
                    "msg": {"type": "string"},
                    "created": {"type": "number"},
                    "version": {"type": "integer", "minimum": 3, "exclusiveMaximum": 4},
                },
                "required": ["version"],
                "additionalProperties": False,
            },
        )
