from typing import Tuple, Union

def parse_version_info(version_str: str) -> Tuple[Union[int, str], ...]:
    parts = version_str.split('.')
    result = []
    rc_suffix = None
    
    for part in parts:
        if part.endswith('rc'):
            rc_suffix = part[:-2]
            result.append(part[:-2])
        else:
            # Convert to integer if it's a number
            try:
                result.append(int(part))
            except ValueError:
                result.append(part)
    
    return tuple(result)