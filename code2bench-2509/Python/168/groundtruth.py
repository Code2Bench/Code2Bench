

def get_parenthetical_substrings(text: str) -> list[str]:
    """
    Finds the all nested parenthetical substrings.

    Args:
        text: The input string to analyze.

    Returns:
        A list of parenthetical substrings.
    """
    substrings = []
    open_paren_indices = []
    for i, char in enumerate(text):
        if char == "(":
            open_paren_indices.append(i)
        elif char == ")" and open_paren_indices:
            start_index = open_paren_indices.pop()
            substrings.append(text[start_index : i + 1])
    return substrings