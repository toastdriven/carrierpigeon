import copy


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
