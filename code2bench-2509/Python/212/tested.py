from typing import Any, List

def prepare_value(value: Any) -> List[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        values = value.strip().split(",")
        return [v.lower() for v in values]
    return value