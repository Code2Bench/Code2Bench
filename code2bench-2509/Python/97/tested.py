from typing import Union

def parse_interval(interval) -> int:
    if isinstance(interval, int):
        return interval
    if not isinstance(interval, str):
        raise ValueError("Interval must be a string or an integer")
    
    # Split the interval into number and unit
    parts = interval.split()
    if len(parts) != 2:
        raise ValueError("Invalid format: must be a string with a number and a unit")
    
    number_str, unit = parts[0], parts[1]
    
    # Convert number to integer
    try:
        number = int(number_str)
    except ValueError:
        raise ValueError("Invalid number in interval") from None
    
    # Define units and their corresponding seconds
    units = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400
    }
    
    # Check if unit is supported
    if unit not in units:
        raise ValueError(f"Unsupported unit: {unit}")
    
    # Calculate total seconds
    return number * units[unit]