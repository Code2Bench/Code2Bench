from typing import List

def compress_token_type_ids(token_type_ids: List[int]) -> int:
    # Check if the list contains only zeros and ones
    if not all(0 <= x <= 1 for x in token_type_ids):
        raise ValueError("Sequence must contain only 0s and 1s")
    
    # Find the first occurrence of 1
    for i, val in enumerate(token_type_ids):
        if val == 1:
            return i
    
    # If no 1 is found, return the length of the list
    return len(token_type_ids)