from typing import List

def digit_version(version_str: str) -> List[int]:
    parts = version_str.split('.')
    result = []
    for part in parts:
        if 'rc' in part:
            base, rc = part.split('rc')
            base = int(base) - 1
            result.append(base)
            result.append(int(rc))
        else:
            result.append(int(part))
    return result