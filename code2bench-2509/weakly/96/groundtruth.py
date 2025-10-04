
from datetime import datetime

def human_date(date_value) -> str:
    """Format a date/datetime to be more human-readable.

    Converts datetime objects or ISO strings to a format like:
    "Jan 15, 2024 at 2:30 PM"
    """
    if not date_value:
        return "—"

    # Handle string datetime values (ISO format)
    if isinstance(date_value, str):
        try:
            # Parse common ISO formats
            for fmt in [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
            ]:
                try:
                    date_value = datetime.strptime(date_value, fmt)
                    break
                except ValueError:
                    continue
            else:
                # If we can't parse it, just return the original truncated string
                return date_value[:16] if len(date_value) > 16 else date_value
        except (ValueError, AttributeError):
            return date_value[:16] if len(date_value) > 16 else date_value

    # Handle datetime objects
    if hasattr(date_value, "strftime"):
        return date_value.strftime("%b %-d, %Y at %-I:%M %p")

    # Fallback for unknown types
    return str(date_value)[:16]