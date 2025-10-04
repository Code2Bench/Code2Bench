from typing import Union, List, Tuple, Any

def flatten_nested_dict_list(d: Union[dict, list], parent_key: str = "", sep: str = "_", item_key: str = "") -> List[Tuple[str, Any]]:
    result = []
    if isinstance(d, dict):
        for key, value in d.items():
            new_key = f"{parent_key}{item_key}{key}" if item_key else f"{parent_key}{key}"
            if isinstance(value, (dict, list)):
                result.extend(flatten_nested_dict_list(value, new_key, sep, item_key))
            else:
                result.append((new_key, value))
    elif isinstance(d, list):
        for i, item in enumerate(d):
            new_key = f"{parent_key}{item_key}{i}" if item_key else f"{parent_key}{i}"
            result.append((new_key, item))
    return result