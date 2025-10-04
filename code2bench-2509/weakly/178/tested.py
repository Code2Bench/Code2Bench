from collections import abc
from typing import Iterable, Type, Optional

def iter_cast(inputs: Iterable, dst_type: Type, return_type: Optional[Type] = None):
    if not isinstance(inputs, abc.Iterable):
        raise TypeError("inputs must be an iterable")
    try:
        casted = [dst_type(item) for item in inputs]
    except (TypeError, ValueError) as e:
        raise TypeError(f"Failed to cast elements to {dst_type}: {e}")
    if return_type is not None:
        if not issubclass(return_type, abc.Iterable):
            raise TypeError("return_type must be an iterable type")
        try:
            return return_type(casted)
        except (TypeError, ValueError) as e:
            raise TypeError(f"Failed to convert result to {return_type}: {e}")
    return casted