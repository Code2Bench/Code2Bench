from re import match

def validate_cses_time(time: str) -> str:
    if match(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$', time):
        return time
    raise ValueError(f"Invalid time format. Expected 'HH:MM:SS', got '{time}'")