from collections import Counter
from typing import Iterable

def f1_score(prediction: Iterable, ground_truth: Iterable, **kwargs) -> float:
    counter_pred = Counter(prediction)
    counter_gt = Counter(ground_truth)
    
    common_elements = set(counter_pred.keys()) & set(counter_gt.keys())
    if not common_elements:
        return 0.0
    
    true_positives = sum(min(counter_pred[e], counter_gt[e]) for e in common_elements)
    precision = true_positives / len(prediction)
    recall = true_positives / len(ground_truth)
    
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0.0
    return f1