import collections

def list_of_flat_dict_to_dict_of_list(list_of_dict: list) -> collections.OrderedDict:
    assert isinstance(list_of_dict, list), "Input must be a list."
    if not list_of_dict:
        return collections.OrderedDict()
    
    # Get the first dictionary to determine the keys
    keys = list_of_dict[0].keys()
    
    # Initialize the result dictionary of lists
    dict_of_list = collections.OrderedDict()
    for key in keys:
        dict_of_list[key] = []
    
    # Populate the lists
    for d in list_of_dict:
        for key in keys:
            dict_of_list[key].append(d[key])
    
    return dict_of_list