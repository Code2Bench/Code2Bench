from typing import Optional

def format_media_duration(total_minutes: Optional[int]) -> str:
    """
    Converts a duration in minutes into a more human-readable format
    (e.g., "1 hour 30 minutes", "45 minutes", "2 hours").

    Args:
        total_minutes: The total duration in minutes (integer).

    Returns:
        A string representing the formatted duration.
    """
    if not total_minutes:
        return "N/A"

    if not isinstance(total_minutes, int) or total_minutes < 0:
        raise ValueError("Input must be a non-negative integer representing minutes.")

    if total_minutes == 0:
        return "0 minutes"

    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []

    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")

    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    # Join the parts with " and " if both hours and minutes are present
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    elif len(parts) == 1:
        return parts[0]
    else:
        # This case should ideally not be reached if total_minutes > 0
        return "0 minutes"  # Fallback for safety, though handled by initial check