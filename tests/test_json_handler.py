import json
import os
import unittest

from carrierpigeon import exceptions
from carrierpigeon.handlers import json as json_handler


CONTRACT_BASE_PATH = os.path.join(os.path.dirname(__file__), "schemas")


class JSONHandlerTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.contract_path = os.path.join(CONTRACT_BASE_PATH, "greeting.v1.json")
        self.jh = json_handler.JSONHandler(self.contract_path)

    def test_from_contract(self):
        title, fields = self.jh.from_contract()
        self.assertIsNotNone(self.jh.schema)
        self.assertEqual(title, "Greeting")
        self.assertEqual(sorted([key for key in fields]), ["greeting", "name", "version"])
        self.assertEqual(fields["greeting"], {"type": "string", "required": False})
        self.assertEqual(fields["name"], {"type": "string", "required": False})
        self.assertEqual(fields["version"], {"type": "number", "required": True})

    def test_read(self):
        # Just handles JSON, doesn't validate.
        data = self.jh.read('{"hello": "world"}')
        self.assertEqual(data, {"hello": "world"})

    def test_write(self):
        # Just handles JSON, doesn't validate.
        msg = self.jh.write({"hello": "world"})
        self.assertEqual(msg, '{"hello": "world"}')

    def test_validate(self):
        # Trigger loading the schema.
        self.jh.from_contract()
        # Shouldn't throw an exception.
        self.jh.validate({"greeting": "Hey", "name": "friendo", "version": 1})

    def test_validate_fails(self):
        # Trigger loading the schema.
        self.jh.from_contract()

        with self.assertRaises(exceptions.ValidationError) as err:
            self.jh.validate({"greeting": "Hey", "name": "friendo"})

            self.assertEqual(len(err.errors), 1)
            self.assertEqual(err.errors[0][0], "version")
            self.assertEqual(err.errors[0][1], "version")
