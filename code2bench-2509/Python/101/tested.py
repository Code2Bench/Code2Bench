def _round_up_to_multiple_of_128_within_limit(x: int, limit: int) -> int:
    import math

    # Check if limit is a multiple of 128 and at least 128
    if limit % 128 != 0 or limit < 128:
        raise AssertionError("limit must be a multiple of 128 and at least 128")

    # Calculate the smallest multiple of 128 greater than or equal to x
    multiple = math.ceil(x / 128) * 128

    # If multiple is less than or equal to limit, return it
    if multiple <= limit:
        return multiple
    else:
        return limit