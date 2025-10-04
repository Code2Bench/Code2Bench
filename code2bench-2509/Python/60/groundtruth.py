from typing import List

def parse_topics_string(topics_string: str) -> List[str]:
    """
    解析话题字符串

    Args:
        topics_string: 话题字符串，用逗号分隔

    Returns:
        话题列表
    """
    if not topics_string:
        return []

    # 分割并清理话题
    topics = [topic.strip() for topic in topics_string.split(",") if topic.strip()]

    # 移除重复话题（保持顺序）
    unique_topics = []
    seen = set()
    for topic in topics:
        if topic not in seen:
            unique_topics.append(topic)
            seen.add(topic)

    return unique_topics