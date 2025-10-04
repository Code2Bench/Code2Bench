import string
from typing import Optional

def decode_base_n(encoded: str, n: int, table: Optional[str] = None) -> int:
    if table is None:
        table = string.digits + string.ascii_lowercase
    if n < 2 or n > len(table):
        raise ValueError("Base must be between 2 and the length of the character table.")
    result = 0
    for char in encoded:
        if char not in table:
            raise ValueError(f"Invalid character '{char}' for base {n}.")
        result = result * n + table.index(char)
    return result