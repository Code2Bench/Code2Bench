
import bisect

import bisect

def _get_padded_token_len(paddings: list[int], x: int) -> int:
    index = bisect.bisect_left(paddings, x)
    assert index < len(paddings)
    return paddings[index]