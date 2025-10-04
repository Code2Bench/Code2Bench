import math

def isqrt(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    x = (n + 1) // 2
    while x * x > n:
        x = (x + n // x) // 2
    return x