def _is_gap_high_quality(gap: str) -> bool:
    gap = gap.strip()
    if len(gap) < 10:
        return False
    if 'general' in gap or 'overview' in gap:
        return False
    words = gap.split()
    if len(words) < 3:
        return False
    return True