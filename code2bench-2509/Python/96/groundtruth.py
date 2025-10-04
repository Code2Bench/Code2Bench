from typing import Any, Dict

def _compute_duration(metrics: Dict[str, Any]) -> float:
    """
    Prefer a single wall-clock measurement if present; otherwise sum only per-step durations.
    Avoid double counting and ignore non-numeric / boolean values.
    """
    wall = metrics.get("total_duration_wall_clock")
    if isinstance(wall, (int, float)):
        return float(wall)

    # Fallback: sum per-step durations only (keys ending with "_duration")
    total = 0.0
    for k, v in metrics.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        if k.endswith("_duration"):
            total += float(v)
    return total