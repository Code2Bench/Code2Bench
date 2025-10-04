from bisect import bisect_left

def closest(value: float | int, sorted_list: list[float | int]) -> float | int:
    index = bisect_left(sorted_list, value)
    candidates = []
    if index > 0:
        candidates.append(sorted_list[index - 1])
    if index < len(sorted_list):
        candidates.append(sorted_list[index])
    return min(candidates, key=lambda x: abs(x - value))