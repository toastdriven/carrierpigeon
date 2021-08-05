import json
import os
import unittest

from carrierpigeon import exceptions
from carrierpigeon import messages
from carrierpigeon.handlers.json import JSONHandler


CONTRACT_BASE_PATH = os.path.join(os.path.dirname(__file__), "schemas")


class SmallTestMessage(messages.BaseMessage):
    # These are usually defined by the factory.
    _fields = {
        "name": {
            "type": "string",
            "required": True,
        },
        "version": {
            "type": "integer",
            "required": True,
        },
    }


class BaseMessageTestCase(unittest.TestCase):
    def test_empty_init(self):
        small = SmallTestMessage()
        self.assertEqual(small._orig_data, {"version": 1})
        self.assertEqual(small._data, {})

    def test_init(self):
        small = SmallTestMessage(name="Daniel")
        self.assertEqual(small._orig_data, {"name": "Daniel", "version": 1})
        self.assertEqual(small._data, {"name": "Daniel"})

    def test_str(self):
        small = SmallTestMessage()
        self.assertEqual(str(small), "SmallTestMessage: {'version': 1}")

    def test_get(self):
        small = SmallTestMessage(name="Daniel")
        self.assertEqual(small.name, "Daniel")

    def test_get_not_present(self):
        small = SmallTestMessage(name="Daniel")

        with self.assertRaises(AttributeError):
            small.foo

    def test_set(self):
        small = SmallTestMessage()
        small.name = "Daniel"
        self.assertEqual(small.all_data(), {"name": "Daniel", "version": 1})

    def test_set_regular_attr(self):
        small = SmallTestMessage()
        small.foo = "bar"
        self.assertEqual(small.all_data(), {"version": 1})
        self.assertEqual(small.foo, "bar")

    def test_del(self):
        small = SmallTestMessage(name="Daniel")
        self.assertEqual(small._data, {"name": "Daniel"})

        del small.name
        self.assertEqual(small._data, {})

    def test_is_dirty(self):
        small = SmallTestMessage(name="Daniel")
        self.assertFalse(small._is_dirty())

        small.name = "Jane"
        self.assertTrue(small._is_dirty())

    def test_all_data(self):
        small = SmallTestMessage()
        self.assertEqual(small.all_data(), {"version": 1})

        small.name = "Daniel"
        self.assertEqual(small.all_data(), {"name": "Daniel", "version": 1})

    def test_from_dict(self):
        small = SmallTestMessage()
        self.assertEqual(small.all_data(), {"version": 1})

        small.from_dict({"name": "Jane", "version": 2})
        self.assertEqual(small.all_data(), {"name": "Jane", "version": 2})

    def test_from_dict_non_field(self):
        small = SmallTestMessage()
        self.assertEqual(small.all_data(), {"version": 1})

        small.from_dict({"msg": "Moof", "version": 2})
        # Note that because `msg` isn't a recognized field, it doesn't end
        # up on the message.
        self.assertEqual(small.all_data(), {"version": 2})


class MessageFactoryTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.contract_path = os.path.join(CONTRACT_BASE_PATH, "greeting.v1.json")
        self.mf = messages.MessageFactory(self.contract_path)

    def test_init(self):
        self.assertEqual(self.mf.schema_path, self.contract_path)
        self.assertTrue(isinstance(self.mf.handler, JSONHandler))
        self.assertEqual(self.mf.message_cls, messages.BaseMessage)

    def test_construct_greeting(self):
        Greeting = self.mf.construct()
        self.assertTrue(issubclass(Greeting, messages.BaseMessage))
        self.assertEqual(sorted([key for key in Greeting._fields]), ["greeting", "name", "version"])
        self.assertEqual(Greeting._handler, self.mf.handler)
        self.assertEqual(Greeting._orig_data, {})
        self.assertEqual(Greeting._data, {})

    def test_read(self):
        Greeting = self.mf.construct()

        read = Greeting.read('{"greeting": "Hi", "name": "planet", "version": 1}')
        self.assertEqual(read.greeting, "Hi")
        self.assertEqual(read.name, "planet")
        self.assertEqual(read.version, 1)

    def test_read_doesnt_affect_class(self):
        Greeting = self.mf.construct()
        read = Greeting.read('{"greeting": "Hi", "name": "planet", "version": 1}')

        # The instance is modified.
        self.assertEqual(read._data["greeting"], "Hi")
        # But the class's data is not (non-shared reference).
        self.assertEqual(Greeting._orig_data, {})
        self.assertEqual(Greeting._data, {})

    def test_read_validation_failed(self):
        Greeting = self.mf.construct()

        with self.assertRaises(exceptions.ValidationError):
            Greeting.read('{"msg": "Hi, planet!", "version": 1}')

    def test_create(self):
        Greeting = self.mf.construct()
        greet = Greeting(greeting="Hey", name="friendo")
        msg = greet.create()
        # We need to load the JSON here, as opposed to a string comparison,
        # because we can't guarantee the key ordering.
        self.assertEqual(json.loads(msg), {"greeting": "Hey", "name": "friendo", "version": 1})


class FunctionsTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.contract_path = os.path.join(CONTRACT_BASE_PATH, "greeting.v1.json")

    def test_message_for(self):
        Greeting = messages.message_for(self.contract_path)
        self.assertTrue(issubclass(Greeting, messages.BaseMessage))
        self.assertEqual(sorted([key for key in Greeting._fields]), ["greeting", "name", "version"])
