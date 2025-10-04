
import math

def _prime_factors(x: int) -> list[int]:
    # find prime factors of axis sizes to help efficiently find divisor chunks
    factors = []
    while x % 2 == 0:
        factors.append(2)
        x //= 2
    for i in range(3, int(math.sqrt(x)) + 1, 2):
        while x % i == 0:
            factors.append(i)
            x //= i
    if x > 1:
        factors.append(x)
    return sorted(factors)