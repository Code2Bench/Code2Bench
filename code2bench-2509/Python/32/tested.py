from typing import Dict, List, Union, Any

def rename_keys(data: Union[Dict, List, Any], key_mapping: Dict[str, str]) -> Union[Dict, List, Any]:
    if isinstance(data, dict):
        # Recursively process each key-value pair
        for key, value in data.items():
            if key in key_mapping:
                data[key] = rename_keys(value, key_mapping)
            else:
                data[key] = value
        return data
    elif isinstance(data, list):
        # Recursively process each element
        new_list = []
        for item in data:
            new_list.append(rename_keys(item, key_mapping))
        return new_list
    else:
        # If not a dictionary or list, return as-is
        return data