from collections import Counter
from typing import Tuple

def compute_token_overlap(prediction: str, reference: str) -> Tuple[int, int, int]:
    prediction_tokens = prediction.split()
    reference_tokens = reference.split()
    
    prediction_counter = Counter(prediction_tokens)
    reference_counter = Counter(reference_tokens)
    
    overlap = sum((prediction_counter & reference_counter).values())
    
    return overlap, len(prediction_tokens), len(reference_tokens)