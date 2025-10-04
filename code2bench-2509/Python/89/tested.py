from typing import List, Tuple

def longest_common_prefix_between_lists_with_elements(list1: List[str], list2: List[str]) -> Tuple[int, Tuple[str, str]]:
    max_length = 0
    best_pair = ()
    
    for s1 in list1:
        for s2 in list2:
            min_len = min(len(s1), len(s2))
            for i in range(min_len):
                if s1[i] != s2[i]:
                    break
            current_length = i
            if current_length > max_length:
                max_length = current_length
                best_pair = (s1, s2)
    
    return (max_length, best_pair)