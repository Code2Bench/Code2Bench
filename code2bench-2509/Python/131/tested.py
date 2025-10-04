from typing import Iterable, Tuple

def nth_combination(iterable: Iterable, r: int, index: int) -> Tuple:
    from itertools import combinations
    
    if r < 0 or r > len(iterable):
        raise ValueError("r must be non-negative and less than or equal to the length of the iterable")
    
    if index < 0:
        raise IndexError("index must be non-negative")
    
    combinations_list = list(combinations(iterable, r))
    if index >= len(combinations_list):
        raise IndexError("index out of range")
    
    return combinations_list[index]