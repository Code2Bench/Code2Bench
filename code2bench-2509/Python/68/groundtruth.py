

def _set_all_properties_required(schema: dict) -> dict:
    """Recursively make all properties required in objects."""
    if not isinstance(schema, dict):
        return schema
    if "properties" in schema:
        schema["required"] = list(schema["properties"].keys())
    for value in schema.values():
        if isinstance(value, dict):
            _set_all_properties_required(value)
        elif isinstance(value, list):
            for item in value:
                _set_all_properties_required(item)
    return schema