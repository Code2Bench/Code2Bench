

def _messages_to_steps(messages: list[dict]) -> list[list[dict]]:
    """Group messages into "pages" as shown by the UI."""
    steps = []
    current_step = []
    for message in messages:
        current_step.append(message)
        if message["role"] == "user":
            steps.append(current_step)
            current_step = []
    if current_step:
        steps.append(current_step)
    return steps