from typing import Dict
from collections import Counter

def calculate_aggregated_metrics(metrics_data: Dict[str, list]) -> Dict[str, Dict]:
    """Calculate aggregated scores for metrics (numeric average or categorical frequency)."""
    agg_metrics = {}
    for metric_name, scores in metrics_data.items():
        # Remove None values
        scores = [score for score in scores if score is not None]
        if not scores:
            avg_score = 0
        elif isinstance(scores[0], (int, float)):
            # Numeric metric - calculate average
            avg_score = sum(scores) / len(scores)
        else:
            # Categorical metric - create frequency distribution
            avg_score = dict(Counter(scores))
        agg_metrics[metric_name] = {"score": avg_score}
    return agg_metrics