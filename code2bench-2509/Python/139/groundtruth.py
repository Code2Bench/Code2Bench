

def diff_dicts(dict1, dict2):
    diff = {}
    for key, value in dict1.items():
        if key not in dict2:
            diff[key] = value
            continue

        try:
            if value != dict2[key]:
                diff[key] = value
        except Exception:
            pass
    return diff