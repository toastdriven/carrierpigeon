import copy


BASE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/unknown.json",
    "title": "",
    "description": "",
    "type": "object",
    "properties": {},
    "required": [],
    "additionalProperties": False,
}


def create_schema(base, filename, fields, required=None, version=None):
    if not required:
        required = []

    new_schema = copy.deepcopy(base)
    new_schema["$id"] = f"https://example.com/{filename}.json"

    name = "".join([bit.capitalize() for bit in [chunk for chunk in filename.split("_")]])
    new_schema["title"] = name

    if version:
        new_schema["$id"] = f"https://example.com/{filename}.v{version}.json"
        new_schema["properties"]["version"] = {
            "type": "integer",
            "minimum": version,
            "exclusiveMaximum": version + 1,
        }
        new_schema["required"].append("version")

    for field in fields:
        new_schema["properties"][field[0]] = {
            "type": field[1],
        }

    new_schema["required"].extend(required)

    return new_schema
