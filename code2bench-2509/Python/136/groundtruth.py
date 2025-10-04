from typing import Any

def _reformat_messages(
    messages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Reformat the content to be compatible with HuggingFaceTokenCounter.

     This function processes a list of messages and converts multi-part
     text content into single string content when all parts are plain text.
     This is necessary for compatibility with HuggingFaceTokenCounter which
     expects simple string content rather than structured content with
     multiple parts.

    Args:
        messages (list[dict[str, Any]]):
            A list of message dictionaries where each message may contain a
            "content" field. The content can be either:
            - A string (unchanged)
            - A list of content items, where each item is a dict that may
                contain "text", "type", and other fields

    Returns:
        list[dict[str, Any]]:
            A list of reformatted messages. For messages where all content
            items are plain text (have "text" field and either no "type"
            field or "type" == "text"), the content list is converted to a
            single newline-joined string. Other messages remain unchanged.

    Example:
        .. code-block:: python

            # Case 1: All text content - will be converted
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"text": "Hello", "type": "text"},
                        {"text": "World", "type": "text"}
                    ]
                }
            ]
            result = _reformat_messages(messages)
            print(result[0]["content"])
            # Output: "Hello\nWorld"

            # Case 2: Mixed content - will remain unchanged
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"text": "Hello", "type": "text"},
                        {"image_url": "...", "type": "image"}
                    ]
                }
            ]

            result = _reformat_messages(messages)  # remain unchanged
            print(type(result[0]["content"]))
            # Output: <class 'list'>

    """
    for message in messages:
        content = message.get("content", [])

        is_all_text = True
        texts = []
        for item in content:
            if not isinstance(item, dict) or "text" not in item:
                is_all_text = False
                break
            if "type" in item and item["type"] != "text":
                is_all_text = False
                break
            if item["text"]:
                texts.append(item["text"])

        if is_all_text and texts:
            message["content"] = "\n".join(texts)

    return messages