import inspect

def _get_valid_kwargs(func: callable, kwargs: dict) -> dict:
    try:
        signature = inspect.signature(func)
        valid_params = set(signature.parameters.keys())
        return {k: v for k, v in kwargs.items() if k in valid_params}
    except (ValueError, TypeError):
        return kwargs