from typing import List

def _prime_factors(x: int) -> List[int]:
    factors = []
    # Handle the case of 2 separately
    while x % 2 == 0:
        factors.append(2)
        x //= 2
    # Check for odd factors starting from 3
    i = 3
    while i * i <= x:
        while x % i == 0:
            factors.append(i)
            x //= i
        i += 2
    # If remaining x is a prime number greater than 2
    if x > 1:
        factors.append(x)
    return factors