from collections import OrderedDict
import json
import os

import jsonschema

from . import base
from .. import exceptions


class JSONHandler(base.BaseHandler):
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

    def write(self, data):
        return json.dumps(data)

    def validate(self, raw_data):
        try:
            jsonschema.validate(instance=raw_data, schema=self.schema)
        except jsonschema.exceptions.ValidationError as err:
            errors = []

            # TODO: Might need to collect multiple errors here.
            errors.append([".".join(err.path), err.message])

            raise exceptions.ValidationError(errors)
