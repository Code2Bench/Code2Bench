def _calculate_temporal_balance(recent: int, evergreen: int) -> str:
    total = recent + evergreen
    if total == 0:
        return "unknown"
    recent_ratio = recent / total
    if recent_ratio > 0.7:
        return "recent_heavy"
    elif recent_ratio < 0.3:
        return "evergreen_heavy"
    else:
        return "balanced"