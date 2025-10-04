

from typing import List

def _get_device_combinations(device_indices):
    devices = sorted(list(device_indices))
    n = len(devices)
    all_combinations = []

    if n == 0:
        return []

    for i in range(1, 1 << n):
        current_combination = []
        for j in range(n):
            if (i >> j) & 1:
                current_combination.append(devices[j])

        if 1 <= len(current_combination) <= n:
            all_combinations.append(current_combination)

    all_combinations.sort(key=lambda combo: (len(combo), combo))

    return all_combinations