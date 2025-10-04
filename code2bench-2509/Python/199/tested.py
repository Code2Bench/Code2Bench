from typing import List, Dict

def _get_confidence_distribution(confidences: List[float]) -> Dict[str, int]:
    high = 0
    medium = 0
    low = 0
    
    for confidence in confidences:
        if confidence >= 0.8:
            high += 1
        elif confidence >= 0.6:
            medium += 1
        else:
            low += 1
    
    return {'high': high, 'medium': medium, 'low': low}