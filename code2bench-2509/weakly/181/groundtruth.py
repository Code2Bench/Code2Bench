
import itertools

import itertools

def get_all_subsets(ring_list):
    all_sub_list = []
    for n_sub in range(len(ring_list)+1):
        all_sub_list.extend(itertools.combinations(ring_list, n_sub))
    return all_sub_list