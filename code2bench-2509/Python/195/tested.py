from typing import Dict

def _rule_based_analysis(previous_text: str, current_text: str) -> Dict[str, float]:
    flow_score = 0.0
    consistency_score = 0.0
    progression_score = 0.0

    # Check for sentence-ending punctuation in previous text
    if previous_text and previous_text[-1] in {'.', '!', '?'}:
        flow_score += 0.1

    # Check for progression keywords in current text
    if any(word in current_text for word in {"therefore", "next"}):
        progression_score += 0.2

    # Check for consistency (current text length)
    if len(current_text.split()) > 120:
        consistency_score += 0.1

    # Check for flow keywords in current text
    if any(word in current_text for word in {"however", "but"}):
        flow_score += 0.1

    # Cap scores at 1.0
    flow_score = min(flow_score, 1.0)
    consistency_score = min(consistency_score, 1.0)
    progression_score = min(progression_score, 1.0)

    return {
        "flow": flow_score,
        "consistency": consistency_score,
        "progression": progression_score
    }