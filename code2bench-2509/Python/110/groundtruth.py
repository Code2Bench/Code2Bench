

def get_termination_value(item):
    if "termination" in item:
        return item["termination"]

    messages = item.get("messages", [])
    if not messages:
        return "unknown"

    last_message = messages[-1]["content"] if messages else ""


    if "max_turns_reached" in last_message.lower():
        return "max_turns_reached"
    elif "max_tokens_reached" in last_message.lower():
        return "max_tokens_reached"
    elif "<answer>" in last_message and "</answer>" in last_message:
        return "answered"
    else:
        return "unknown"