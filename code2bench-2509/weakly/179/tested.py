from functools import cache

def format_seconds(seconds: int) -> str:
    @cache
    def format_time(s: int) -> str:
        hours = s // 3600
        remaining_seconds = s % 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        components = []
        if hours > 0:
            components.append(f"{hours}h")
        if minutes > 0:
            components.append(f"{minutes}m")
        if seconds > 0:
            components.append(f"{seconds}s")
        return " ".join(components)
    return format_time(seconds)