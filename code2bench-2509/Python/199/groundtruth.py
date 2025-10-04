from typing import Dict, List

from typing import List, Dict

def _get_confidence_distribution(confidences: List[float]) -> Dict[str, int]:
    """Get distribution of confidence scores."""
    distribution = {'high': 0, 'medium': 0, 'low': 0}

    for confidence in confidences:
        if confidence >= 0.8:
            distribution['high'] += 1
        elif confidence >= 0.6:
            distribution['medium'] += 1
        else:
            distribution['low'] += 1

    return distribution