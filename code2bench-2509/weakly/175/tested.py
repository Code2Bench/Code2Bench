import regex

def extract_multi_choice_answer(pred_str: str) -> str:
    # Remove text following "Problem:"
    pred_str = regex.sub(r'Problem:.+', '', pred_str).strip()
    # Replace "choice is" with "answer is"
    pred_str = pred_str.replace("choice is", "answer is")
    # Search for pattern "answer is" followed by a single letter (a, b, c, d, or e)
    match = regex.search(r'answer is ([abcde])', pred_str)
    if match:
        return match.group(1).upper()
    return "placeholder"