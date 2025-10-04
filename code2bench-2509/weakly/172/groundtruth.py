
from bisect import bisect_left

from bisect import bisect_left

def closest(value, sorted_list):
    index = bisect_left(sorted_list, value)
    if index == 0:
        return sorted_list[0]
    elif index == len(sorted_list):
        return sorted_list[-1]
    else:
        value_before = sorted_list[index - 1]
        value_after = sorted_list[index]
        if value_after - value < value - value_before:
            return value_after
        else:
            return value_before