import math

def format_bytes_to_human_readable(bytes: int) -> str:
    if bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    factor = 1024
    exponent = 0
    
    while bytes >= factor:
        bytes /= factor
        exponent += 1
    
    return f"{bytes:.2f} {units[exponent]}"