from typing import List, Tuple

def binary_search(candidates: List[int], target: int) -> Tuple[List[int], int]:
    trajectory = []
    left = 0
    right = len(candidates) - 1
    
    while left <= right:
        mid = (left + right) // 2
        trajectory.append((left, right, mid))
        
        if candidates[mid] == target:
            break
        elif candidates[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return trajectory, candidates[left]