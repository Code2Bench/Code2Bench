

def longest_common_prefix_with_lengths(list1, list2):
    """计算两个二维列表中每个子列表的最长前缀匹配长度，并记录拥有最长前缀匹配长度的两个子列表的长度
    :param list1: 第一个二维列表
    :param list2: 第二个二维列表
    :return: 最长前缀匹配长度以及拥有最长前缀匹配长度的两个子列表的长度
    """
    max_length = 0
    len_list1 = 0
    len_list2 = 0
    for i, sublist1 in enumerate(list1):
        for j, sublist2 in enumerate(list2):
            match_length = 0
            min_length = min(len(sublist1), len(sublist2))
            for k in range(min_length):
                if sublist1[k] == sublist2[k]:
                    match_length += 1
                else:
                    break
            if match_length > max_length:
                max_length = match_length
                len_list1 = len(sublist1)
                len_list2 = len(sublist2)
    return max_length, len_list1, len_list2