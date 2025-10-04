
from datetime import datetime

def iso8601_to_epoch_ms(iso8601_string: str) -> int:
    """
    Convert ISO 8601 string to epoch milliseconds (matches Java iso8601StringToEpochLong).

    Args:
        iso8601_string: ISO 8601 formatted datetime string

    Returns:
        Time as epoch milliseconds
    """
    dt = datetime.fromisoformat(iso8601_string.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)