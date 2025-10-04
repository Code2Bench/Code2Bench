from typing import Dict, Any

def parse_hp_string(hp_string: str) -> Dict[str, Any]:
    items = hp_string.split(',')
    result = {}
    for item in items:
        if '.' in item:
            key, value = item.split('.')
            result[key] = parse_hp_string(value)
        else:
            key, value = item.split('=')
            result[key] = convert_to_type(value)
    return result

def convert_to_type(value: str) -> Any:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            try:
                return bool(value)
            except ValueError:
                return value
    return value