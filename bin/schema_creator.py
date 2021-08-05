#!/usr/bin/env python
import json

from carrierpigeon import utils


if __name__ == "__main__":
    filename = input("Desired filename ('.json' assumed): ").strip()
    version = int(input("Version number [1]: ").strip())

    if not version:
        version = 1

    print()

    fields = []
    required = []

    while True:
        fieldname = input("Field name (blank to finish): ").strip()

        if not fieldname:
            break

        field_type = input("Field type [string]: ").strip()

        if not field_type:
            field_type = "string"

        fields.append([fieldname, field_type])
        is_required = input(f"Is '{fieldname}' required [y/N]: ").strip()

        if is_required.lower().startswith("y"):
            required.append(fieldname)

        print()

    print()
    print("-----")
    print()

    schema = utils.create_schema(utils.BASE_SCHEMA, filename, fields, required, version=version)
    print(json.dumps(schema, indent=4))
