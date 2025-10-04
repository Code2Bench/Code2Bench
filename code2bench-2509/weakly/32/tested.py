import string

def format_int_alpha(value: int) -> str:
    assert isinstance(value, int) and value > 0, "value must be a positive integer"
    letters = string.ascii_lowercase
    result = []
    while value > 0:
        value -= 1
        result.append(letters[value % 26])
        value //= 26
    return ''.join(reversed(result))