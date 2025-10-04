

def _get_quality_grade(quality_score: float) -> str:
    """Get quality grade from score."""
    if quality_score >= 0.9:
        return 'A'
    elif quality_score >= 0.8:
        return 'B'
    elif quality_score >= 0.7:
        return 'C'
    elif quality_score >= 0.6:
        return 'D'
    else:
        return 'F'