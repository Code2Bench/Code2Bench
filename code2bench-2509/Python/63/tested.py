from typing import Dict, Any

def format_metrics_safe(metrics: Dict[str, Any]) -> str:
    result = []
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            formatted_value = f"{value:.4f}"
        else:
            formatted_value = str(value)
        result.append(f"{key}={formatted_value}")
    return ",".join(result) if result else ""