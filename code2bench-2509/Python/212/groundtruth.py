

def prepare_value(value):
    """Convert JSON list to list of selected values."""
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # Handle legacy comma-separated string format
        return [day.strip().lower() for day in value.split(",") if day.strip()]
    return value