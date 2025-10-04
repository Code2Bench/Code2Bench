from typing import Tuple
from collections import Counter

def compute_token_overlap(prediction: str, reference: str) -> Tuple[int, int, int]:
    """
    Compute token overlap between prediction and reference.

    Args:
        prediction: Predicted answer.
        reference: Reference answer.

    Returns:
        A tuple of (number of overlapping tokens, number of prediction tokens, number of reference tokens).
    """
    prediction_tokens = prediction.split()
    reference_tokens = reference.split()

    common = Counter(prediction_tokens) & Counter(reference_tokens)
    num_same = sum(common.values())

    return num_same, len(prediction_tokens), len(reference_tokens)