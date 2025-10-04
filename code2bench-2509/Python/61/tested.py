def validate_word_constraint(text: str, N: int, quantifier: str) -> bool:
    # Strip leading and trailing whitespace from the text
    cleaned_text = text.strip()
    
    # Split the text into words
    words = cleaned_text.split()
    
    # Get the actual word count
    actual_words = len(words)
    
    if quantifier == "at least":
        return actual_words >= N
    elif quantifier == "at most":
        return actual_words <= N
    elif quantifier == "around":
        tolerance = int(0.1 * N)
        # For "around", the tolerance is the maximum of 10% of N or 1 word
        tolerance = max(tolerance, 1)
        return abs(actual_words - N) <= tolerance
    else:
        raise ValueError("Invalid quantifier. Must be one of 'at least', 'at most', or 'around'.")