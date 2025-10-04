from typing import List, Tuple

def remove_duplicates(data_list: List[Tuple[int, Tuple[int, int], int, Tuple[int, int]]]) -> List[Tuple[int, Tuple[int, int], int, Tuple[int, int]]]:
    seen = set()
    result = []
    for item in data_list:
        key = (item[0], item[3])
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result