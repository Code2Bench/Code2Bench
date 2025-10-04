

def flatten_nested_dict_list(d, parent_key="", sep="_", item_key=""):
    """
    Flatten a nested dict or list to a list.

    For example, given a dict
    {
        a: 1
        b: {
            c: 2
        }
        c: 3
    }

    the function would return [(a, 1), (b_c, 2), (c, 3)]

    Args:
        d (dict, list): a nested dict or list to be flattened
        parent_key (str): recursion helper
        sep (str): separator for nesting keys
        item_key (str): recursion helper
    Returns:
        list: a list of (key, value) tuples
    """
    items = []
    if isinstance(d, (tuple, list)):
        new_key = parent_key + sep + item_key if len(parent_key) > 0 else item_key
        for i, v in enumerate(d):
            items.extend(flatten_nested_dict_list(v, new_key, sep=sep, item_key=str(i)))
        return items
    elif isinstance(d, dict):
        new_key = parent_key + sep + item_key if len(parent_key) > 0 else item_key
        for k, v in d.items():
            assert isinstance(k, str)
            items.extend(flatten_nested_dict_list(v, new_key, sep=sep, item_key=k))
        return items
    else:
        new_key = parent_key + sep + item_key if len(parent_key) > 0 else item_key
        return [(new_key, d)]