from typing import Optional

def _calculate_phrase_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0
    
    # Convert both texts to lowercase for case-insensitive comparison
    text1_lower = text1.lower()
    text2_lower = text2.lower()
    
    # Split texts into words
    words1 = text1_lower.split()
    words2 = text2_lower.split()
    
    # Define the list of two-word and three-word phrases to check
    two_word_phrases = set()
    three_word_phrases = set()
    
    # Generate all two-word and three-word phrases from text1
    for i in range(len(words1) - 1):
        two_word_phrases.add((words1[i], words1[i+1]))
        if i + 2 < len(words1):
            three_word_phrases.add((words1[i], words1[i+1], words1[i+2]))
    
    # Check if any phrase from text1 exists in text2
    similarity = 0.0
    
    for phrase in two_word_phrases:
        if phrase in three_word_phrases:
            similarity += 0.15
        elif phrase in two_word_phrases:
            similarity += 0.1
    
    # Cap the similarity score at 0.3
    return min(similarity, 0.3)