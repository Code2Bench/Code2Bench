def time_to_24hrtime(hhmmss: str) -> str:
    # Check if the input contains a colon
    if ':' not in hhmmss:
        return hhmmss
    
    # Split the string into hours, minutes, seconds, and AM/PM
    parts = hhmmss.split(':')
    hour_str, minute_str, second_str = parts[0], parts[1], parts[2]
    
    # Extract AM/PM
    am_pm = parts[-1].lower()
    
    # Convert AM/PM to 24-hour format
    if am_pm == 'pm':
        if hour_str == '12':
            hour = '00'
        else:
            hour = str(int(hour_str) + 12)
    else:
        if hour_str == '12':
            hour = '00'
        else:
            hour = hour_str
    
    # Combine the parts into the final format
    return f"{hour}:{minute_str}:{second_str}"