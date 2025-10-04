from typing import Iterable

def _expand_iterable(original, num_desired, default) -> list:
    if not isinstance(original, Iterable) or isinstance(original, str):
        return [default] * num_desired
    else:
        return list(original) + [default] * (num_desired - len(original))