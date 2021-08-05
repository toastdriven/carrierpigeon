import json
import os
import unittest

from carrierpigeon import exceptions
from carrierpigeon import libraries
from carrierpigeon import messages


CONTRACT_BASE_PATH = os.path.join(os.path.dirname(__file__), "schemas")


class LibrariesTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.library = libraries.Library(CONTRACT_BASE_PATH)

    def test_init(self):
        self.assertEqual(self.library.base_contract_dir, CONTRACT_BASE_PATH)
        self.assertEqual(self.library._classes, {})

    def test_check_exists(self):
        # No exception should be raised.
        self.library.check_exists()

    def test_check_exists_fails(self):
        with self.assertRaises(exceptions.InvalidContractDirectory):
            library = libraries.Library("/path/to/invalid/contracts/dir/")
            library.check_exists()

    def test_collect_contracts(self):
        contracts = self.library.collect_contracts()
        self.assertTrue(len(contracts) > 0)
        self.assertTrue(os.path.join(CONTRACT_BASE_PATH, "greeting.v1.json") in contracts)

    def test_load(self):
        Greeting = self.library.load(os.path.join(CONTRACT_BASE_PATH, "greeting.v1.json"))
        self.assertTrue(issubclass(Greeting, messages.BaseMessage))

    def test_load_all(self):
        library = libraries.Library.load_all(CONTRACT_BASE_PATH)
        self.assertTrue(len(library._classes) > 0)
        self.assertTrue("Greeting" in library._classes)
        self.assertTrue("PostCreated" in library._classes)

    def test_get(self):
        library = libraries.Library.load_all(CONTRACT_BASE_PATH)
        # Ensure the new class is present.
        self.assertTrue(issubclass(library.Greeting, messages.BaseMessage))

    def test_available_classes(self):
        library = libraries.Library.load_all(CONTRACT_BASE_PATH)
        self.assertTrue("Greeting" in library.available_classes())
        self.assertTrue("PostCreated" in library.available_classes())


class LibrariesFunctionsTestCase(unittest.TestCase):
    def test_load_library(self):
        library = libraries.load_library(CONTRACT_BASE_PATH)
        self.assertTrue("Greeting" in library.available_classes())
