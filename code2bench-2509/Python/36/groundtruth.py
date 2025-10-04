

def align_ampersands(str1, str2):
    """
    This function takes two strings containing various "&" characters and transforms them so that the indices of "&"
    are aligned. This is useful for formatting LaTeX tables.

    Args:
        str1 (str): First input string containing "&" characters.
        str2 (str): Second input string containing "&" characters.

    Returns:
        Tuple[str, str]: Two transformed strings with aligned "&" indices.
    """
    # Find indices of "&" characters in both strings
    amp_idx1 = [i for i, char in enumerate(str1) if char == "&"]
    amp_idx2 = [i for i, char in enumerate(str2) if char == "&"]

    assert len(amp_idx1) == len(amp_idx2)

    # Replace "&" characters in the strings with "\&" at the aligned indices
    acc1, acc2 = 0, 0
    for i, j in zip(amp_idx1, amp_idx2):
        diff = (j + acc2) - (i + acc1)
        if diff > 0:
            str1 = str1[: i + acc1] + " " * diff + str1[i + acc1 :]
            acc1 += diff
        elif diff < 0:
            str2 = str2[: j + acc2] + " " * (-diff) + str2[j + acc2 :]
            acc2 -= diff

    return str1, str2