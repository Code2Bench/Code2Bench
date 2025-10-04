

def seconds_to_time_string(seconds: int):
    """
    Converts seconds to a time string. e.g. 1 hour 2 minutes, 1 hour 2 seconds, 1 hour, 1 minute 2 seconds, etc.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        if minutes > 0:
            return f"{hours} hr{'s' if hours > 1 else ''}, {minutes} min{'s' if minutes > 1 else ''}"

        return f"{hours} hr{'s' if hours > 1 else ''}"

    if minutes > 0:
        return f"{minutes} min{'s' if minutes > 1 else ''}"

    return f"{remaining_seconds} sec"