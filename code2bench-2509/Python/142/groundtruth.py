

def deep_merge(defaults, current):
    """Recursively merge defaults into current, overwriting type mismatches and adding missing fields."""
    if not isinstance(defaults, dict) or not isinstance(current, dict):
        return defaults
    merged = dict(current)
    for k, v in defaults.items():
        if k not in merged:
            merged[k] = v
        else:
            if isinstance(v, dict) and isinstance(merged[k], dict):
                merged[k] = deep_merge(v, merged[k])
            elif type(merged[k]) != type(v):
                merged[k] = v
    # Optionally remove keys not in defaults (strict sync)
    # for k in list(merged.keys()):
    #     if k not in defaults:
    #         del merged[k]
    return merged