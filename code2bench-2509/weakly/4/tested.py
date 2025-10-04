import bisect
from typing import List, Tuple

def find_chunk_index(chunks: List[Tuple[int, int]], idx: int) -> int:
    left = 0
    right = len(chunks)
    while left < right:
        mid = (left + right) // 2
        if chunks[mid][1] < idx:
            left = mid + 1
        else:
            right = mid
    if left == len(chunks) or chunks[left][0] > idx:
        raise ValueError("Index not found in any chunk")
    return left