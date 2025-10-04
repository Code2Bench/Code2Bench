from typing import List

def _generate_episode_range_string(episode_indices: List[int]) -> str:
    # Deduplicate the list
    unique_indices = list(set(episode_indices))
    unique_indices.sort()
    
    # Handle empty case
    if not unique_indices:
        return "无"
    
    result = []
    i = 0
    
    while i < len(unique_indices):
        # Find the end of the range
        j = i
        while j + 1 < len(unique_indices) and unique_indices[j+1] == unique_indices[j] + 1:
            j += 1
        
        # Add the range to the result
        if i == j:
            result.append(str(unique_indices[i]))
        else:
            result.append(f"{unique_indices[i]}-{unique_indices[j]}")
        
        # Move to the next element
        i = j + 1
    
    return ",".join(result)