from typing import List, Optional

def match_size(image_size: List[List[int]], h: int, w: int) -> Optional[List[int]]:
    min_diff = float('inf')
    best_size = None
    
    for size in image_size:
        width, height = size
        
        # Calculate the difference in maximum dimensions
        max_dim_diff = abs(max(width, height) - max(h, w))
        
        # Calculate the difference in aspect ratio
        aspect_ratio_diff = abs((width / height) - (w / h))
        
        # Update the best size if this size has a smaller difference
        if max_dim_diff < min_diff or (max_dim_diff == min_diff and aspect_ratio_diff < min_diff):
            min_diff = max_dim_diff
            best_size = size
    
    return best_size if best_size else None