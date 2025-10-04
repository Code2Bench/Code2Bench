from typing import List, Dict, Any

def list_of_dict_to_dict_of_list(list_of_dict: List[Dict[Any, Any]]) -> Dict[Any, List[Any]]:
    result = {}
    for dict_in_list in list_of_dict:
        for key, value in dict_in_list.items():
            if key not in result:
                result[key] = []
            result[key].append(value)
    return result