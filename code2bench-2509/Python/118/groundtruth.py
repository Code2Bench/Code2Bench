

def human_count(n: int) -> str:
    if n < 0:
        return str(n)
    if n < 1_000:
        return str(n)
    for label, scale in (("T", 1_000_000_000_000),
                         ("B", 1_000_000_000),
                         ("M", 1_000_000),
                         ("K", 1_000)):
        if n >= scale:
            return f"{n/scale:.2f}{label}"

    return str(n)