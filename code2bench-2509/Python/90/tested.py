from typing import List, Tuple

def longest_common_prefix_with_lengths(list1: List[List[int]], list2: List[List[int]]) -> Tuple[int, int, int]:
    max_prefix_length = 0
    max_list1_length = 0
    max_list2_length = 0

    for sublist1 in list1:
        for sublist2 in list2:
            prefix_length = 0
            while prefix_length < min(len(sublist1), len(sublist2)) and sublist1[prefix_length] == sublist2[prefix_length]:
                prefix_length += 1
            if prefix_length > max_prefix_length:
                max_prefix_length = prefix_length
                max_list1_length = len(sublist1)
                max_list2_length = len(sublist2)

    return (max_prefix_length, max_list1_length, max_list2_length)