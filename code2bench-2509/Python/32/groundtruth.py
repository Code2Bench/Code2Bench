

def rename_keys(data, key_mapping):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = key_mapping.get(key, key)
            new_data[new_key] = rename_keys(value, key_mapping)
        return new_data
    elif isinstance(data, list):
        return [rename_keys(item, key_mapping) for item in data]
    else:
        return data