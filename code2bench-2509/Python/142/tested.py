from typing import Dict, Any

def deep_merge(defaults: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for key, value in defaults.items():
        if key in current:
            if isinstance(value, dict) and isinstance(current[key], dict):
                result[key] = deep_merge(value, current[key])
            else:
                result[key] = value
        else:
            result[key] = value
    return result