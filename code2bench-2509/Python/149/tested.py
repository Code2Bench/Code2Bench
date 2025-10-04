import math

def format_timer(secs: float) -> str:
    if secs < 0:
        return ""
    
    seconds = int(secs)
    days = seconds // (24 * 3600)
    remaining_seconds = seconds % (24 * 3600)
    
    hours = remaining_seconds // 3600
    remaining_seconds %= 3600
    
    minutes = remaining_seconds // 60
    seconds_remaining = remaining_seconds % 60
    
    if days > 0:
        return f"{days} days"
    elif hours > 0:
        return f"{hours} hrs"
    elif minutes > 0:
        return f"{minutes} mins"
    else:
        return f"{seconds_remaining} secs"