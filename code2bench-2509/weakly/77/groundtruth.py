from typing import Optional
import string

def encode_base_n(num: int, n: int, table: Optional[str] = None) -> str:
    """
    Encode a number in base-n representation.

    Args:
        num: The number to encode
        n: The base to use for encoding
        table: Custom character table (optional)

    Returns:
        String representation of the number in base-n

    Examples:
        >>> encode_base_n(255, 16)
        'ff'
        >>> encode_base_n(42, 36)
        '16'
    """
    if table is None:
        # Default table: 0-9, a-z
        table = string.digits + string.ascii_lowercase

    if not 2 <= n <= len(table):
        raise ValueError(f"Base must be between 2 and {len(table)}")

    if num == 0:
        return table[0]

    result = []
    is_negative = num < 0
    num = abs(num)

    while num > 0:
        result.append(table[num % n])
        num //= n

    if is_negative:
        result.append("-")

    return "".join(reversed(result))