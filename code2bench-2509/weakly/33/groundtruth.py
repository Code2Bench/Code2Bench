
from re import match

def validate_cses_time(time: str) -> str:
    regex = r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d)"
    if match(regex, time):
        return time
    raise ValueError({"need": repr(regex), "got": time})