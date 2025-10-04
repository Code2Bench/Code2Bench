from typing import Optional
from datetime import datetime

def format_timestamp(timestamp: Optional[int]) -> Optional[str]:
    """Format Unix timestamp to ISO format string."""
    if timestamp is None:
        return None

    try:
        return datetime.fromtimestamp(timestamp / 1000).isoformat()
    except Exception as e:
        return str(f'Error: {e}, Timestamp: {timestamp}')  # Return as string if conversion fails