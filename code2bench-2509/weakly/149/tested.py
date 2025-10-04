from math import isqrt

def generate_primes(max_num: int) -> list[int]:
    if max_num < 2:
        return []
    sieve = [True] * (max_num + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(max_num) + 1):
        if sieve[i]:
            for j in range(i*i, max_num + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]