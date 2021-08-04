import glob
import os

from . import exceptions
from . import messages


class Library(object):
    def __init__(self, base_schema_dir):
        self.base_schema_dir = base_schema_dir
        self._classes = {}

    def __getattr__(self, possible_class):
        if possible_class in self._classes:
            return self._classes[possible_class]

        return super().__getattr__(possible_class)

    def check_exists(self):
        if not os.path.exists(self.base_schema_dir):
            raise exceptions.InvalidSchemaDirectory(f"No schemas found at {self.base_schema_dir}")

    def collect_schemas(self):
        return glob.glob(os.path.join(self.base_schema_dir, "*.json"))

    def load(self, schema):
        return messages.message_for(schema)

    def available_classes(self):
        return [key for key in self._classes]

    @classmethod
    def load_all(cls, base_schema_dir):
        obj = cls(base_schema_dir)
        obj.check_exists()
        schema_paths = obj.collect_schemas()

        for schema_path in schema_paths:
            klass = obj.load(schema_path)
            obj._classes[klass.__name__] = klass

        return obj


def load_library(base_schema_dir):
    return Library.load_all(base_schema_dir)
