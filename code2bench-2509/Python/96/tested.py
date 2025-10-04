from typing import Dict, Any

def _compute_duration(metrics: Dict[str, Any]) -> float:
    total = 0.0

    # Check for wall-clock measurement
    if "wall_clock" in metrics:
        return metrics["wall_clock"]

    # Sum all valid per-step durations
    for key, value in metrics.items():
        if key.endswith("_duration") and isinstance(value, (int, float)):
            total += value

    return total