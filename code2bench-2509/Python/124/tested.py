from typing import Dict, Any, Union

def flatten_state_dict(obj: Union[dict, list, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    result = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            result[new_key] = flatten_state_dict(value, new_key, sep)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            new_key = f"{parent_key}.{i}" if parent_key else f"{parent_key}.{i}"
            result[new_key] = flatten_state_dict(value, new_key, sep)
    else:
        result[parent_key] = obj
    return result