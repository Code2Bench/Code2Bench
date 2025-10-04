def _fix_a_slash_b(string: str) -> str:
    if '/' in string:
        numerator, denominator = string.split('/', 1)
        if numerator.count('sqrt') > 0 or denominator.count('sqrt') > 0:
            return f'\\frac{{{numerator}}}{denominator}'
        try:
            numerator_int = int(numerator)
            denominator_int = int(denominator)
            return f'\\frac{{{numerator_int}}}{denominator_int}'
        except ValueError:
            return string
    else:
        return string