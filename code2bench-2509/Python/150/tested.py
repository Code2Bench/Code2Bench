import math

def format_mins_timer(mins: float) -> str:
    if mins < 0:
        return ""
    
    minutes = int(round(mins))
    seconds = int(round(mins * 60))
    
    if minutes == 0:
        return "0 min"
    
    if seconds == 0:
        return f"{minutes} min"
    
    # Determine the largest unit
    units = []
    if minutes >= 60:
        units.append("hr")
        minutes -= 60
    if minutes >= 60:
        units.append("day")
        minutes -= 60
    if minutes >= 60:
        units.append("week")
        minutes -= 60
    if minutes >= 60:
        units.append("month")
        minutes -= 60
    if minutes >= 60:
        units.append("year")
        minutes -= 60
    
    if not units:
        return f"{minutes} min"
    
    # Format the output
    if len(units) == 1:
        return f"{minutes} {units[0]}"
    else:
        return f"{minutes} {units[0]}{'' if len(units) == 2 else 's'}"