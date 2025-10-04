from typing import List

def build_buckets(mantissa_lst: List[int], max_value: int) -> List[int]:
    buckets = []
    for mantissa in mantissa_lst:
        value = mantissa * 10 ** 0
        if value > max_value:
            break
        buckets.append(value)
    return buckets