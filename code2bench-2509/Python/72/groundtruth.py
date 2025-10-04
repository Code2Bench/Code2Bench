from typing import List

def _generate_episode_range_string(episode_indices: List[int]) -> str:
    """
    将分集编号列表转换为紧凑的字符串表示形式。
    例如: [1, 2, 3, 5, 8, 9, 10] -> "1-3, 5, 8-10"
    """
    if not episode_indices:
        return "无"

    indices = sorted(list(set(episode_indices)))
    if not indices:
        return "无"

    ranges = []
    start = end = indices[0]

    for i in range(1, len(indices)):
        if indices[i] == end + 1:
            end = indices[i]
        else:
            ranges.append(str(start) if start == end else f"{start}-{end}")
            start = end = indices[i]
    ranges.append(str(start) if start == end else f"{start}-{end}")
    return ", ".join(ranges)