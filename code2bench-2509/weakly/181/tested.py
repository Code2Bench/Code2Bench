import itertools

def get_all_subsets(ring_list: list) -> list:
    subsets = []
    for r in range(len(ring_list) + 1):
        for subset in itertools.combinations(ring_list, r):
            subsets.append(subset)
    return subsets