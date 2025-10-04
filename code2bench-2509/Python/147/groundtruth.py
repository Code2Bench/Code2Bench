

def pretty_format_ns(value: int) -> str:
    """Pretty formats a time value in nanoseconds to human readable value."""
    if value < 1000:
        return f"{value}ns"
    elif value < 1000_000:
        return f"{value/1000:.2f}us"
    elif value < 1_000_000_000:
        return f"{value/1000_000:.2f}ms"
    else:
        return f"{value/1000_000_000:.2f}s"