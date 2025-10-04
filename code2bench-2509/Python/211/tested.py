from typing import List

def _get_device_combinations(device_indices: List[int]) -> List[List[int]]:
    # Sort the device indices to ensure consistent ordering in the output
    device_indices.sort()
    
    # Generate all possible non-empty combinations of device indices
    from itertools import combinations
    
    combinations_list = []
    for i in range(1, len(device_indices) + 1):
        combinations_list.extend(combinations(device_indices, i))
    
    return combinations_list