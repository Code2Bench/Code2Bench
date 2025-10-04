import math

def format_size(bytes_size: int) -> str:
    if bytes_size == 0:
        return "0.0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    scale = 1024
    size = bytes_size
    unit_index = 0
    
    while size >= scale:
        size /= scale
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"