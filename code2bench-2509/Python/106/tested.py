from typing import Tuple

def factorization(dimension: int, factor: int = -1) -> Tuple[int, int]:
    if dimension <= 0:
        raise ValueError("Dimension must be a positive integer.")
    
    if factor == -1:
        # Find the most balanced pair of factors
        m = int(dimension ** 0.5)
        while m * m < dimension:
            m += 1
        n = dimension // m
        return (m, n)
    
    if dimension % factor != 0:
        # If the factor does not divide the dimension evenly, find the closest possible pair
        m = factor
        while m * m < dimension:
            m += 1
        n = dimension // m
        return (m, n)
    
    # If the factor divides the dimension evenly and is less than or equal to the square root of the dimension
    return (factor, dimension // factor)