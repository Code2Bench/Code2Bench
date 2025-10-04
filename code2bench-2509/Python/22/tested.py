def fix_sqrt(string: str) -> str:
    import re
    return re.sub(r'\\sqrt(\S+)', r'\\sqrt{\1}', string)