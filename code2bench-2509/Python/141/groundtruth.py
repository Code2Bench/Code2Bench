

def count_todos(obj) -> int:
    """Count TODO: translate entries in a dict or list."""
    if isinstance(obj, dict):
        return sum(count_todos(v) for v in obj.values())
    if isinstance(obj, list):
        return sum(count_todos(v) for v in obj)
    if isinstance(obj, str) and obj.strip().startswith("TODO: translate"):
        return 1
    return 0