import math

def _human_bytes(n: float) -> str:
    if n < 0:
        raise ValueError("Byte count must be non-negative")
    
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    factor = 1024.0
    unit_index = 0
    
    while n >= factor:
        n /= factor
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(n)}B"
    else:
        return f"{round(n, 2)}{units[unit_index]}"