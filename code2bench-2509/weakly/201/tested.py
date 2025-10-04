import collections
from typing import List, Dict, Any

def list_of_flat_dict_to_dict_of_list(list_of_dict: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    assert isinstance(list_of_dict, list), "Input must be a list"
    result = collections.defaultdict(list)
    for d in list_of_dict:
        for key, value in d.items():
            result[key].append(value)
    return dict(result)