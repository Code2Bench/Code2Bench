

def extract_content_string(content):
    """
    从各种消息格式中提取字符串内容
    Extract string content from various message formats

    Args:
        content: 消息内容，可能是字符串、列表或其他格式

    Returns:
        str: 提取的字符串内容
    """
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Handle Anthropic's list format
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                item_type = item.get('type')  # 缓存type值
                if item_type == 'text':
                    text_parts.append(item.get('text', ''))
                elif item_type == 'tool_use':
                    tool_name = item.get('name', 'unknown')  # 缓存name值
                    text_parts.append(f"[Tool: {tool_name}]")
            else:
                text_parts.append(str(item))
        return ' '.join(text_parts)
    else:
        return str(content)