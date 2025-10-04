

def parse_version(version_str: str) -> tuple[int, int, int]:
    """
    Parse version string to tuple of integers for comparison.

    Args:
        version_str: Version string like "5.5.5"

    Returns:
        Tuple of (major, minor, patch) as integers
    """
    try:
        parts = version_str.strip().split(".")
        if len(parts) >= 3:
            return (int(parts[0]), int(parts[1]), int(parts[2]))
        elif len(parts) == 2:
            return (int(parts[0]), int(parts[1]), 0)
        elif len(parts) == 1:
            return (int(parts[0]), 0, 0)
        else:
            return (0, 0, 0)
    except (ValueError, IndexError):
        return (0, 0, 0)