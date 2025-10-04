from datetime import datetime

def calculate_task_duration(start_time: str, end_time: str) -> str:
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
    except ValueError:
        return "Invalid time format. Please use HH:MM format."
    
    duration = end - start
    hours = duration.seconds // 3600
    minutes = (duration.seconds // 60) % 60
    
    return f"{hours} hours and {minutes} minutes"