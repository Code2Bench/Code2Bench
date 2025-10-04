

def similarity_score(s1: str, s2: str) -> float:
    """Fast similarity score based on common prefix and suffix.
    Returns lower score for more similar strings."""
    # Find common prefix length
    prefix_len = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            break
        prefix_len += 1

    # Find common suffix length if strings differ in middle
    if prefix_len < min(len(s1), len(s2)):
        s1_rev = s1[::-1]
        s2_rev = s2[::-1]
        suffix_len = 0
        for c1, c2 in zip(s1_rev, s2_rev):
            if c1 != c2:
                break
            suffix_len += 1
    else:
        suffix_len = 0

    # Return inverse similarity - shorter common affix means higher score
    return len(s1) + len(s2) - 2.0 * (prefix_len + suffix_len)