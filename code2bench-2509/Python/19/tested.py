from typing import List

def find_closest_aspect_ratio(aspect_ratio: float, target_ratios: List[List[int]], width: int, height: int, image_size: int) -> List[int]:
    def calculate_difference(ratio: List[int]) -> float:
        w, h = ratio
        return abs((w / h) - aspect_ratio)
    
    def calculate_area(ratio: List[int]) -> float:
        w, h = ratio
        return w * h
    
    closest_ratio = None
    min_diff = float('inf')
    max_area = 0
    
    for ratio in target_ratios:
        diff = calculate_difference(ratio)
        area = calculate_area(ratio)
        
        if diff < min_diff:
            min_diff = diff
            closest_ratio = ratio
        elif diff == min_diff:
            if area > max_area:
                max_area = area
                closest_ratio = ratio
    
    return closest_ratio