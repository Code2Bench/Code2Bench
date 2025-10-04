def _fix_sqrt(string: str) -> str:
    import re
    # Use regular expression to find all occurrences of \\sqrt
    # and ensure that the argument is enclosed in curly braces
    return re.sub(r'\\sqrt{(.*?)}', r'\\sqrt{\1}', string)