
from collections.abc import Iterable, Sized

from typing import Iterable

def _expand_iterable(original, num_desired, default):
    if isinstance(original, Iterable) and not isinstance(original, str):
        return original + [default] * (num_desired - len(original))
    else:
        return [default] * num_desired