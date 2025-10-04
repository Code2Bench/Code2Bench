import itertools
from typing import List, Tuple

def get_one_prot_diff_name_pairs(names: List[str]) -> List[Tuple[str, str]]:
    pairs = []
    for name1, name2 in itertools.combinations(names, 2):
        charge1 = int(name1.split('_')[1])
        charge2 = int(name2.split('_')[1])
        if abs(charge1 - charge2) == 1:
            pairs.append((name1, name2))
    return pairs