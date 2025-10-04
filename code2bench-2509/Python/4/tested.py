from typing import Tuple

def parse_version(version_str: str) -> Tuple[int, int, int]:
    if not version_str:
        return (0, 0, 0)
    
    parts = version_str.split('.')
    return tuple(map(int, parts + [0])) if len(parts) < 3 else tuple(map(int, parts))