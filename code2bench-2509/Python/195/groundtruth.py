from typing import Dict

from typing import Dict

def _rule_based_analysis(previous_text: str, current_text: str) -> Dict[str, float]:
    flow = 0.6
    consistency = 0.6
    progression = 0.6

    if previous_text and previous_text[-1] in ".!?":
        flow += 0.1
    if any(k in current_text.lower() for k in ["therefore", "next", "building on", "as a result", "furthermore", "additionally"]):
        progression += 0.2
    if len(current_text.split()) > 120:
        consistency += 0.1
    if any(k in current_text.lower() for k in ["however", "but", "although", "despite"]):
        flow += 0.1

    return {
        "flow": min(flow, 1.0),
        "consistency": min(consistency, 1.0),
        "progression": min(progression, 1.0),
    }