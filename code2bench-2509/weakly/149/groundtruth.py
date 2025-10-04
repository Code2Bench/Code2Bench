
from math import isqrt

from math import isqrt

def generate_primes(max_num: int) -> list[int]:
    are_primes = [True] * (max_num + 1)
    are_primes[0] = are_primes[1] = False
    for i in range(2, isqrt(max_num) + 1):
        if are_primes[i]:
            for j in range(i * i, max_num + 1, i):
                are_primes[j] = False

    return [prime for prime, is_prime in enumerate(are_primes) if is_prime]