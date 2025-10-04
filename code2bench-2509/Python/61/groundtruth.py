

def validate_word_constraint(text: str, N: int, quantifier: str) -> bool:
    """
    Reference implementation from: https://github.com/allenai/open-instruct/blob/main/open_instruct/if_functions.py
    """
    # 清除多余空白字符并拆分文本为单词列表
    words = text.strip().split()
    actual_count = len(words)

    # 定义 "around" 约束的容错范围（目标单词数的 ±10%，至少 1 个单词）
    tolerance = max(round(N * 0.1), 1)

    if quantifier == "at least":
        return actual_count >= N
    elif quantifier == "at most":
        return actual_count <= N
    elif quantifier == "around":
        return abs(actual_count - N) <= tolerance
    else:
        return False