from typing import Optional

def pretty_format_ns(value: int) -> str:
    if value < 1000:
        return f"{value} ns"
    elif 1000 <= value < 1_000_000:
        return f"{value / 1000:.2f} us"
    elif 1_000_000 <= value < 1_000_000_000:
        return f"{value / 1_000_000:.2f} ms"
    else:
        return f"{value / 1_000_000_000:.2f} s"