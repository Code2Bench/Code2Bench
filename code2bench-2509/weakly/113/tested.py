from math import log

def ratio_to_db(ratio: float | int, val2: float | int = None, using_amplitude: bool = True) -> float:
    if val2 is not None:
        ratio = ratio / val2
    if ratio == 0:
        return float('-inf')
    if using_amplitude:
        return 20 * log(ratio)
    else:
        return 10 * log(ratio)