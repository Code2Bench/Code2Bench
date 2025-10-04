from typing import Optional

def time_str_to_secs(time_str: str = None) -> int:
    if time_str is None or time_str == "":
        return 0
    
    # Dictionary to map units to seconds
    unit_to_seconds = {
        "sec": 1,
        "s": 1,
        "seconds": 1,
        "second": 1,
        "min": 60,
        "minutes": 60,
        "min": 60,
        "minute": 60,
        "hrs": 3600,
        "hours": 3600,
        "hr": 3600,
        "hour": 3600
    }
    
    # Split the time string into parts
    parts = time_str.split()
    if len(parts) < 2:
        return 0
    
    # Get the base value and unit
    base_value = int(parts[0])
    unit = parts[1]
    
    # Check if the unit is valid
    if unit not in unit_to_seconds:
        return 0
    
    # Calculate the total seconds
    return base_value * unit_to_seconds[unit]