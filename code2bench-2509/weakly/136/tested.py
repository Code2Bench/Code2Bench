from typing import List

def _parse_api_keys(api_keys: str) -> List[str]:
    if not api_keys:
        return []
    return [key.strip() for key in api_keys.split(',')]