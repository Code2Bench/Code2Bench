from datetime import datetime

def iso8601_to_epoch_ms(iso8601_string: str) -> int:
    if 'Z' in iso8601_string:
        iso8601_string = iso8601_string.replace('Z', '+00:00')
    dt = datetime.fromisoformat(iso8601_string)
    return int(dt.timestamp() * 1000)