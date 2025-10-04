from typing import Dict, Any

def _extract_message_text(msg: Dict[str, Any]) -> str:
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        result = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                result.append(item.get("text"))
            elif isinstance(item, dict) and item.get("type") == "image_url":
                result.append("[IMAGE]")
            else:
                result.append(str(item))
        return " ".join(result)
    return str(content)