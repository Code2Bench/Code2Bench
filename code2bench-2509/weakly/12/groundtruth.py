from typing import Dict
from typing import Dict, Any, Optional, List, Tuple
from copy import deepcopy

def _deep_merge_dicts(source: Dict, destination: Dict) -> Dict:
    """
    Recursively merges the 'source' dictionary into the 'destination' dictionary.
    Keys from 'source' will overwrite existing keys in 'destination'.
    If a key in 'source' corresponds to a dictionary, a recursive merge is performed.
    The 'destination' dictionary is modified in place.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            if isinstance(
                node, dict
            ):  # Ensure the destination node is a dict for merging
                _deep_merge_dicts(value, node)
            else:  # If destination's node is not a dict, overwrite it entirely
                destination[key] = deepcopy(value)
        else:
            destination[key] = value
    return destination