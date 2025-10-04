

def longest_common_prefix_between_lists_with_elements(list1, list2):
    """计算两个字符串列表中元素的最长前缀匹配长度
    :param list1:
    :param list2:
    :return:
    """
    max_prefix_length = 0
    max_prefix_elements = ()
    for str1 in list1:
        for str2 in list2:
            prefix_length = 0
            min_len = min(len(str1), len(str2))
            for i in range(min_len):
                if str1[i] == str2[i]:
                    prefix_length += 1
                else:
                    break
            if prefix_length > max_prefix_length:
                max_prefix_length = prefix_length
                max_prefix_elements = (str1, str2)
    return max_prefix_length, max_prefix_elements