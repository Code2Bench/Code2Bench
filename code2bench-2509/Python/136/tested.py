from typing import Any, List, Dict

def _reformat_messages(
    messages: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    reformatted = []
    for message in messages:
        if "content" in message:
            content = message["content"]
            if all(item.get("text") for item in content):
                # All content is plain text
                formatted_content = "\n".join(item["text"] for item in content)
                reformatted.append({
                    **message,
                    "content": formatted_content
                })
            else:
                # Some content is not plain text
                reformatted.append(message)
        else:
            # No content field, leave as is
            reformatted.append(message)
    return reformatted