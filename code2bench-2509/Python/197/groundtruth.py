

def _is_gap_high_quality(gap: str) -> bool:
    gap = gap.strip()

    # Length check
    if len(gap) < 10:
        return False

    # Generic gap check
    generic_gaps = ['general', 'overview', 'introduction', 'basics', 'fundamentals']
    if gap.lower() in generic_gaps:
        return False

    # Check for meaningful content
    if len(gap.split()) < 3:
        return False

    return True