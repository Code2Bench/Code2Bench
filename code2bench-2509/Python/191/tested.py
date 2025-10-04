def _recommend_timing_profile(confidence: float) -> str:
    if confidence >= 0.8:
        return "stealth"
    elif 0.5 <= confidence < 0.8:
        return "conservative"
    elif 0.2 <= confidence < 0.5:
        return "normal"
    else:
        return "aggressive"