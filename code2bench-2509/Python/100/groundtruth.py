

def extract_weave_refs_from_value(value):
    """Extract all strings that start with 'weave:///' from a value."""
    refs = []
    if isinstance(value, str) and value.startswith("weave:///"):
        refs.append(value)
    elif isinstance(value, dict):
        for v in value.values():
            refs.extend(extract_weave_refs_from_value(v))
    elif isinstance(value, list):
        for v in value:
            refs.extend(extract_weave_refs_from_value(v))
    return refs