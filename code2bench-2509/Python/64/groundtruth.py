from typing import Any, Dict

def format_improvement_safe(parent_metrics: Dict[str, Any], child_metrics: Dict[str, Any]) -> str:
    """
    Safely format improvement metrics for logging.

    Args:
        parent_metrics: Parent program metrics
        child_metrics: Child program metrics

    Returns:
        Formatted string representation of improvements
    """
    if not parent_metrics or not child_metrics:
        return ""

    improvement_parts = []
    for metric, child_value in child_metrics.items():
        if metric in parent_metrics:
            parent_value = parent_metrics[metric]
            # Only calculate improvement for numeric values
            if isinstance(child_value, (int, float)) and isinstance(parent_value, (int, float)):
                try:
                    diff = child_value - parent_value
                    improvement_parts.append(f"{metric}={diff:+.4f}")
                except (ValueError, TypeError):
                    # Skip non-numeric comparisons
                    continue

    return ", ".join(improvement_parts)