from typing import List

def format_index_ranges(indices: List[int]) -> str:
    if not indices:
        return ""
    
    result = []
    i = 0
    while i < len(indices):
        start = indices[i]
        j = i + 1
        while j < len(indices) and indices[j] == indices[j - 1] + 1:
            j += 1
        end = indices[j - 1]
        
        if i == 0:
            result.append(f"{start}-{end}")
        else:
            result.append(f",{start}-{end}")
        
        i = j
    
    return ",".join(result)