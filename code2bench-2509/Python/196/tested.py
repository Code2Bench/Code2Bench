from typing import Optional

def _heuristic_transition(previous_text: str, current_heading: str) -> str:
    # Extract the last 240 characters of previous_text
    previous_text = previous_text[-240:] if len(previous_text) > 240 else previous_text
    
    # Check for keywords in the previous text
    has_challenge = any(word in previous_text for word in ["problem", "issue", "challenge"])
    has_solution = any(word in previous_text for word in ["solution", "approach", "method"])
    has_important = any(word in previous_text for word in ["important", "crucial", "essential"])
    
    # Determine the transition sentence based on keywords
    if has_challenge:
        return f"Identifying challenges and exploring potential solutions to {current_heading}."
    elif has_solution:
        return f"Building on the approach of {current_heading} to find effective solutions."
    elif has_important:
        return f"Emphasizing the importance of {current_heading} in addressing key issues."
    else:
        return f"Introducing {current_heading} as a relevant and important topic."