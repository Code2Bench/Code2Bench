

def validate_and_extract_os_classifiers(classifiers: list) -> list:
    os_classifiers = [c for c in classifiers if c.startswith("Operating System :: ")]
    if not os_classifiers:
        return []

    os_values = [c[len("Operating System :: ") :] for c in os_classifiers]
    valid_os_prefixes = {"Microsoft", "POSIX", "MacOS", "OS Independent"}

    for os_value in os_values:
        if not any(os_value.startswith(prefix) for prefix in valid_os_prefixes):
            return []

    return os_values