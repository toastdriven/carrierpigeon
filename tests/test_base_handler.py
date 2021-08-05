import unittest

from carrierpigeon.handlers import base


class BaseHandlerTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.bh = base.BaseHandler("/path/to/whatever")

    def test_init(self):
        self.assertEqual(self.bh.schema_path, "/path/to/whatever")
        self.assertIsNone(self.bh.schema)

    def test_from_contract(self):
        with self.assertRaises(NotImplementedError):
            self.bh.from_contract()

    def test_read(self):
        with self.assertRaises(NotImplementedError):
            self.bh.read("")

    def test_write(self):
        with self.assertRaises(NotImplementedError):
            self.bh.write({})

    def test_validate(self):
        with self.assertRaises(NotImplementedError):
            self.bh.validate({})
