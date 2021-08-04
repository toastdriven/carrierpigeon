import builtins
import copy
import json


BASE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/unknown.json",
    "title": "",
    "description": "",
    "type": "object",
    "properties": {"version": {"type": "number"}},
    "required": ["version"],
}


def create_schema(base, filename, fields, required=None):
    if not required:
        required = []

    new_schema = copy.deepcopy(base)
    new_schema["$id"] = f"https://example.com/{filename}.json"

    name = "".join([bit.capitalize() for bit in [chunk for chunk in filename.split("_")]])
    new_schema["title"] = name

    for field in fields:
        new_schema["properties"][field[0]] = {
            "type": field[1],
        }

    new_schema["required"].extend(required)

    return new_schema


if __name__ == "__main__":
    filename = input("Desired filename: ")

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

    schema = create_schema(BASE_SCHEMA, filename, fields, required)
    print(json.dumps(schema, indent=4))
