from typing import Tuple

def seconds_to_time_string(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    return f"{hours} hr{'s' if hours > 1 else ''} {minutes} min{'s' if minutes > 1 else ''} {remainder} sec{'s' if remainder > 1 else ''}"