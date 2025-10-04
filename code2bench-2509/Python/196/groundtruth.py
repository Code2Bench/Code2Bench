

def _heuristic_transition(previous_text: str, current_heading: str) -> str:
    tail = previous_text[-240:]
    if any(word in tail.lower() for word in ["problem", "issue", "challenge"]):
        return f"Now that we've identified the challenges, let's explore {current_heading.lower()} to find solutions."
    elif any(word in tail.lower() for word in ["solution", "approach", "method"]):
        return f"Building on this approach, {current_heading.lower()} provides the next step in our analysis."
    elif any(word in tail.lower() for word in ["important", "crucial", "essential"]):
        return f"Given this importance, {current_heading.lower()} becomes our next focus area."
    else:
        return (
            f"Building on the discussion above, this leads us into {current_heading.lower()}, "
            f"where we focus on practical implications and what to do next."
        )