

def _recommend_timing_profile(confidence: float) -> str:
    if confidence >= 0.8:
        return "stealth"
    elif confidence >= 0.5:
        return "conservative"
    elif confidence >= 0.2:
        return "normal"
    else:
        return "aggressive"