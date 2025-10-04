def shquote(arg: str) -> str:
    # Check for special characters or spaces
    if ' ' in arg or '"' in arg or "'" in arg or '\\' in arg or '#' in arg:
        return f"'{arg}'"
    return arg