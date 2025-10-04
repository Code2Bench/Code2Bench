
import inspect

import inspect

def _get_valid_kwargs(func, kwargs):
    try:
        sig = inspect.signature(func)
        param_keys = set(sig.parameters.keys())
        return {k: v for k, v in kwargs.items() if k in param_keys}
    except (ValueError, TypeError):
        return kwargs