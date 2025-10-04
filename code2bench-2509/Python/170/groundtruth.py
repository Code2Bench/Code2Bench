

def update_yaml_dict(yaml_dict, vocabulary):
    for key, value in vocabulary.items():
        if key not in yaml_dict:
            yaml_dict[key] = value
        elif isinstance(value, dict) and isinstance(yaml_dict[key], dict):
            update_yaml_dict(yaml_dict[key], value)
    return yaml_dict