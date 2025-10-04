from collections.abc import Mapping

def flatten_results_dict(results: dict) -> dict:
    flattened = {}
    
    def _flatten(d: Mapping, parent_key: str = ""):
        for key, value in d.items():
            new_key = f"{parent_key}/{key}" if parent_key else key
            if isinstance(value, Mapping):
                _flatten(value, new_key)
            else:
                flattened[new_key] = value
    
    _flatten(results)
    return flattened