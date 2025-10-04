from typing import Dict, Any

def format_dict_to_string(data: dict, indent_level: int = 0, use_colon: bool = True) -> str:
    if not isinstance(data, dict):
        return str(data)
    
    result = []
    for key, value in data.items():
        if use_colon:
            result.append(f"{key}: ")
        else:
            result.append(f"{key} ")
        
        if isinstance(value, dict):
            result.append("{")
            result.extend(format_dict_to_string(value, indent_level + 1, use_colon))
            result.append("}")
        else:
            result.append(str(value))
        
        if use_colon:
            result.append("\n")
        else:
            result.append("\n")
    
    return "".join(result).rstrip()