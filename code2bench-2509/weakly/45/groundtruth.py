
import itertools

def get_one_prot_diff_name_pairs(names):
    """
    Get all pairs of names that have a charge difference of 1.

    Assumes that the names are in the format "name_charge_spin"
    """
    name_pairs = []
    for name0, name1 in itertools.combinations(names, 2):
        name0_charge = int(name0.split("_")[-2])
        name1_charge = int(name1.split("_")[-2])
        if abs(name0_charge - name1_charge) == 1:
            name_pairs.append((name0, name1))
    return name_pairs