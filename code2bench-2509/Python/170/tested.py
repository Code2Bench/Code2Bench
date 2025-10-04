from typing import Dict, Any

def update_yaml_dict(yaml_dict: Dict[str, Any], vocabulary: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in vocabulary.items():
        if key in yaml_dict:
            if isinstance(yaml_dict[key], dict) and isinstance(value, dict):
                update_yaml_dict(yaml_dict[key], value)
            else:
                yaml_dict[key] = value
        else:
            yaml_dict[key] = value
    return yaml_dict