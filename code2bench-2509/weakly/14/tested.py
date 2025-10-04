from typing import List, Tuple
import itertools

def _pad_version(left: List[str], right: List[str]) -> Tuple[List[str], List[str]]:
    max_len = max(len(left), len(right))
    left += ['0'] * (max_len - len(left))
    right += ['0'] * (max_len - len(right))
    return left, right