
from datetime import datetime

def epoch_ms_to_utc_iso(ms: int) -> str:
    """Convert milliseconds since epoch to an ISO 8601 timestamp string."""
    # Use replace to convert 'Z' suffix to '+00:00' for compatibility with fromisoformat()
    iso_string = datetime.datetime.fromtimestamp(ms / 1000.0, tz=datetime.timezone.utc).isoformat()
    # Ensure the timezone is represented as +00:00 instead of +00:00 (if it's already that way)
    # or convert Z to +00:00 if the isoformat() method ever returns Z
    if iso_string.endswith('Z'):
        iso_string = iso_string[:-1] + '+00:00'
    return iso_string