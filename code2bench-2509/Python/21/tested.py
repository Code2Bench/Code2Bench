def fix_fracs(string: str) -> str:
    import re
    # Use regular expression to find all fractions
    fractions = re.findall(r'\\frac{(.*?)\((.*?)\))', string)
    # Replace each fraction with properly formatted one
    processed = re.sub(r'\\frac{(.*?)\((.*?)\))', r'\\frac{{{0}}}}{{{1}}}'.format(*match), string)
    return processed