from collections.abc import MutableMapping

def flatten_dict(dictionary: MutableMapping, prefix: str = "", sep: str = "_") -> dict:
    result = {}
    for key, value in dictionary.items():
        new_key = f"{prefix}{sep}{key}" if prefix else key
        if isinstance(value, MutableMapping):
            result.update(flatten_dict(value, new_key, sep))
        else:
            result[new_key] = value
    return result