from typing import Optional

def format_media_duration(total_minutes: Optional[int]) -> str:
    if total_minutes is None:
        return "N/A"
    
    if total_minutes < 0:
        raise ValueError("total_minutes must be a non-negative integer")
    
    hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    
    if hours == 0:
        return f"{remaining_minutes} minutes"
    elif remaining_minutes == 0:
        return f"{hours} hours"
    else:
        return f"{hours} hours and {remaining_minutes} minutes"