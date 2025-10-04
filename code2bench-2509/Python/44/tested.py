from typing import List, Dict

def _messages_to_steps(messages: List[Dict]) -> List[List[Dict]]:
    steps = []
    current_step = []

    for message in messages:
        if message['role'] == 'user':
            if current_step:
                steps.append(current_step)
                current_step = []
            current_step.append(message)
        else:
            if current_step:
                steps.append(current_step)
                current_step = []
            current_step.append(message)

    if current_step:
        steps.append(current_step)

    return steps