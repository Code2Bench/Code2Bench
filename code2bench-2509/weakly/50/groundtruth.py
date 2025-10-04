
from collections.abc import MutableMapping

def flatten_dict(dictionary, prefix="", sep="_"):
    results = []
    for k, v in dictionary.items():
        new_key = str(prefix) + sep + str(k) if prefix else k
        if isinstance(v, MutableMapping):
            results.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            results.append((new_key, v))
    return dict(results)