from collections import OrderedDict

def strip_module(state_dict: dict) -> OrderedDict:
    ordered_dict = OrderedDict()
    for key, value in state_dict.items():
        if key.startswith('module.'):
            new_key = key[7:]
            ordered_dict[new_key] = value
        else:
            ordered_dict[key] = value
    return ordered_dict