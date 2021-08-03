from collections import OrderedDict
import json
import os

import jsonschema


class JSONHandler(object):
    def __init__(self, schema_path=None):
        self.schema_path = schema_path
        self.schema = None

    def from_contract(self):
        schema = OrderedDict()

        with open(self.schema_path) as raw_schema_file:
            raw_schema = json.loads(raw_schema_file.read())
            self.schema = raw_schema

            title = raw_schema.get("title", os.path.basename(self.schema_path).capitalize())

            for prop_name, prop_info in raw_schema.get("properties", {}).items():
                schema[prop_name] = {
                    "type": prop_info.get("type", "string"),
                }
                schema[prop_name].setdefault("required", False)

            for required_prop_name in raw_schema.get("required", []):
                schema.setdefault(required_prop_name, {})
                schema[required_prop_name].setdefault("required", True)

        return title, schema

    def read(self, raw_msg):
        return json.loads(raw_msg)

    def validate(self, raw_data):
        jsonschema.validate(instance=raw_data, schema=self.schema)
