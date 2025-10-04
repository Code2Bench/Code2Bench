

def trim_schema(schema: dict) -> dict:
    # Turn JSON Schema from MCP generated into Harmony's variant.
    if "title" in schema:
        del schema["title"]
    if "default" in schema and schema["default"] is None:
        del schema["default"]
    if "anyOf" in schema:
        # Turn "anyOf": [{"type": "type-1"}, {"type": "type-2"}] into "type": ["type-1", "type-2"]
        # if there's more than 1 types, also remove "null" type as Harmony will just ignore it
        types = [
            type_dict["type"] for type_dict in schema["anyOf"]
            if type_dict["type"] != 'null'
        ]
        schema["type"] = types
        del schema["anyOf"]
    if "properties" in schema:
        schema["properties"] = {
            k: trim_schema(v)
            for k, v in schema["properties"].items()
        }
    return schema