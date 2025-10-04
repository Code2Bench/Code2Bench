from typing import List

def parse_topics_string(topics_string: str) -> List[str]:
    # Split the string by commas and strip whitespace from each topic
    topics = [topic.strip() for topic in topics_string.split(',') if topic.strip()]
    # Remove duplicates while preserving order
    unique_topics = []
    seen = set()
    for topic in topics:
        if topic not in seen:
            seen.add(topic)
            unique_topics.append(topic)
    return unique_topics