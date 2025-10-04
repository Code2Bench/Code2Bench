

def format_bytes_to_human_readable(bytes: int) -> str:
    if bytes > 1000 * 1000 * 1000 * 1000:
        return f"{bytes / (1000 * 1000 * 1000 * 1000):.2f} TB"
    if bytes > 1000 * 1000 * 1000:
        return f"{bytes / (1000 * 1000 * 1000):.2f} GB"
    elif bytes > 1000 * 1000:
        return f"{bytes / (1000 * 1000):.2f} MB"
    elif bytes > 1000:
        return f"{bytes / 1000:.2f} KB"
    else:
        return f"{bytes} B"