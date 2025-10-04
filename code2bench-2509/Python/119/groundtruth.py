

def _human_bytes(n: float) -> str:
    if n <= 0:
        return "0B"

    for unit in ["B","KB","MB","GB","TB","PB"]:
        if n < 1024:
            return f"{n:.0f}{unit}" if unit == "B" else f"{n:.2f}{unit}"
        n /= 1024.0

    return f"{n:.2f}PB"