
import operator
from functools import reduce

from functools import reduce
import operator

def get_in(keys, coll, default=None, no_default=False):
    try:
        return reduce(operator.getitem, keys, coll)
    except (KeyError, IndexError, TypeError):
        if no_default:
            raise
        return default