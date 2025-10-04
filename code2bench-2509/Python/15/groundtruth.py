

def _truncate(value: str, max_chars: int, ellipsis: str) -> str:
    if max_chars is None:
        return value
    if max_chars <= 0:
        return ""
    if len(value) <= max_chars:
        return value
    # Ensure final length <= max_chars considering ellipsis
    ell = ellipsis or ""
    if len(ell) >= max_chars:
        # Ellipsis doesn't fit; hard cut
        return value[:max_chars]
    cut = max_chars - len(ell)
    return value[:cut] + ell