from typing import Any, Union

def flatten(obj: Union[dict, list, Any], parent_key: str = "", sep: str = ".") -> dict:
    result = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            result.update(flatten(value, new_key, sep))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            new_key = f"{parent_key}.{index}" if parent_key else f"{index}"
            result.update(flatten(value, new_key, sep))
    else:
        result[parent_key] = obj
    return result