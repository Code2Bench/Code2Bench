

def get_messages_summary(messages: list[dict]) -> dict:
    """
    Get summary statistics about messages without returning all data.

    Args:
        messages: Full list of messages

    Returns:
        Summary statistics
    """
    if not messages:
        return {"total": 0, "by_type": {}, "by_model": {}, "total_tokens": 0}

    by_type = {}
    by_model = {}
    total_tokens = 0

    for msg in messages:
        # Count by type
        msg_type = msg.get("type", "unknown")
        by_type[msg_type] = by_type.get(msg_type, 0) + 1

        # Count by model
        model = msg.get("model", "unknown")
        by_model[model] = by_model.get(model, 0) + 1

        # Sum tokens
        tokens = msg.get("tokens", {})
        if isinstance(tokens, dict):
            total_tokens += tokens.get("input", 0) + tokens.get("output", 0)

    return {"total": len(messages), "by_type": by_type, "by_model": by_model, "total_tokens": total_tokens}