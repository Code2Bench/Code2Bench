from typing import Optional
import string

def decode_base_n(encoded: str, n: int, table: Optional[str] = None) -> int:
    """
    Decode a base-n encoded string back to an integer.

    Args:
        encoded: The base-n encoded string
        n: The base used for encoding
        table: Custom character table (optional)

    Returns:
        The decoded integer

    Examples:
        >>> decode_base_n('ff', 16)
        255
        >>> decode_base_n('16', 36)
        42
    """
    if table is None:
        table = string.digits + string.ascii_lowercase

    if not 2 <= n <= len(table):
        raise ValueError(f"Base must be between 2 and {len(table)}")

    if not encoded:
        return 0

    is_negative = encoded.startswith("-")
    if is_negative:
        encoded = encoded[1:]

    result = 0
    for i, char in enumerate(reversed(encoded.lower())):
        if char not in table:
            raise ValueError(f"Invalid character '{char}' for base {n}")

        digit_value = table.index(char)
        if digit_value >= n:
            raise ValueError(f"Invalid digit '{char}' for base {n}")

        result += digit_value * (n**i)

    return -result if is_negative else result