import copy


BASE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/unknown.json",
    "title": "",
    "description": "",
    "type": "object",
    "properties": {"version": {"type": "number", "minimum": 1, "exclusiveMaximum": 2}},
    "required": ["version"],
}


def create_schema(base, filename, fields, required=None, version=1):
    if not required:
        required = []

    new_schema = copy.deepcopy(base)
    new_schema["$id"] = f"https://example.com/{filename}.json"

    name = "".join([bit.capitalize() for bit in [chunk for chunk in filename.split("_")]])
    new_schema["title"] = name

    if version:
        new_schema["$id"] = f"https://example.com/{filename}.v{version}.json"
        new_schema["properties"]["version"]["minimum"] = version
        new_schema["properties"]["version"]["exclusiveMaximum"] = version + 1

    for field in fields:
        new_schema["properties"][field[0]] = {
            "type": field[1],
        }

    new_schema["required"].extend(required)

    return new_schema
