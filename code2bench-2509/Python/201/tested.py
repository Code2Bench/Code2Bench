def _get_quality_grade(quality_score: float) -> str:
    if 0.9 <= quality_score <= 1.0:
        return "A"
    elif 0.8 <= quality_score < 0.9:
        return "B"
    elif 0.7 <= quality_score < 0.8:
        return "C"
    elif 0.6 <= quality_score < 0.7:
        return "D"
    else:
        return "F"