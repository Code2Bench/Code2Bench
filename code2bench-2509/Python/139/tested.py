from typing import Dict

def diff_dicts(dict1: dict, dict2: dict) -> dict:
    result = {}
    for key, value in dict1.items():
        if key not in dict2:
            result[key] = value
        elif value != dict2[key]:
            result[key] = value
    return result