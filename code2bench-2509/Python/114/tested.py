from typing import List

def CalculateAlpha(
    distances: List[float],
    fade_end: float = 10,
    fade_start: float = 30,
    max_fade_start: float = 150,
    max_fade_end: float = 170,
    verbose: bool = False,
) -> float:
    if not distances:
        return 0.0
    
    average_distance = sum(distances) / len(distances)
    
    if average_distance < fade_end:
        return 0.0
    elif fade_end < average_distance < fade_start:
        return (average_distance - fade_end) / (fade_start - fade_end) * 255.0
    elif fade_start < average_distance < max_fade_start:
        return 255.0
    elif max_fade_start < average_distance < max_fade_end:
        return 255.0 - (average_distance - max_fade_start) / (max_fade_end - max_fade_start) * 255.0
    else:
        return 0.0