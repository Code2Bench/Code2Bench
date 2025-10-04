import copy
import bisect

def _quantize(x: list, bins: list) -> list:
    sorted_bins = sorted(bins)
    return [bisect.bisect_right(sorted_bins, value) for value in x]