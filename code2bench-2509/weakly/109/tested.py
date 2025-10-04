from datetime import datetime
from typing import Optional

def format_timestamp(timestamp: Optional[int]) -> Optional[str]:
    if timestamp is None:
        return None
    try:
        # Convert milliseconds to seconds
        seconds = timestamp / 1000
        # Create datetime object
        dt = datetime.utcfromtimestamp(seconds)
        # Format to ISO string
        return dt.isoformat()
    except Exception as e:
        return str(e)