import math

def _format_file_size(size_bytes: int) -> str:
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    if size_bytes == 0:
        return '0 B'
    
    unit_index = 0
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{size_bytes:.1f} B"
    else:
        return f"{size_bytes:.1f} {units[unit_index]}"