from typing import Iterable, Optional, Type
import abc

from collections import abc
from typing import Iterable, Type, Optional

def iter_cast(inputs: Iterable, dst_type: Type, return_type: Optional[Type] = None):
    if not isinstance(inputs, abc.Iterable):
        raise TypeError('inputs must be an iterable object')
    if not isinstance(dst_type, type):
        raise TypeError('"dst_type" must be a valid type')

    out_iterable = map(dst_type, inputs)

    if return_type is None:
        return out_iterable
    else:
        return return_type(out_iterable)