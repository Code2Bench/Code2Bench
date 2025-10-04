import string
from typing import Optional

def encode_base_n(num: int, n: int, table: Optional[str] = None) -> str:
    if table is None:
        table = string.digits + string.ascii_lowercase
    if n < 2 or n > len(table):
        raise ValueError("Base must be between 2 and the length of the character table.")
    if num == 0:
        return table[0]
    result = []
    is_negative = False
    if num < 0:
        is_negative = True
        num = -num
    while num > 0:
        remainder = num % n
        result.append(table[remainder])
        num //= n
    if is_negative:
        result.append('-')
    return ''.join(reversed(result))