from collections import Counter
from typing import Dict

def calculate_aggregated_metrics(metrics_data: Dict[str, list]) -> Dict[str, Dict]:
    result = {}
    for metric, scores in metrics_data.items():
        valid_scores = [score for score in scores if score is not None]
        if not valid_scores:
            result[metric] = {"score": 0}
            continue
        if all(isinstance(score, (int, float)) for score in valid_scores):
            average = sum(valid_scores) / len(valid_scores)
            result[metric] = {"score": average}
        else:
            frequency = Counter(valid_scores)
            result[metric] = {"score": dict(frequency)}
    return result