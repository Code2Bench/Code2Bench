def human_count(n: int) -> str:
    if n < 1:
        return str(n)
    scale = 0
    if n >= 1_000_000_000:
        scale = 3
    elif n >= 1_000_000:
        scale = 6
    elif n >= 1_000:
        scale = 3
    else:
        scale = 0
    value = n / 10**scale
    return f"{value:.2f}{['K', 'M', 'B', 'T'][scale]}"