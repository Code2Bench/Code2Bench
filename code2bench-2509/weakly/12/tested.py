from typing import Dict
from copy import deepcopy

def _deep_merge_dicts(source: Dict, destination: Dict) -> Dict:
    for key, value in source.items():
        if key in destination:
            if isinstance(destination[key], dict) and isinstance(value, dict):
                _deep_merge_dicts(value, destination[key])
            else:
                destination[key] = value
        else:
            destination[key] = value
    return destination