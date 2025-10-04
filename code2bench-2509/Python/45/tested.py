def _fix_fracs(string: str) -> str:
    return string.replace("\\frac", "\\frac{}{}")