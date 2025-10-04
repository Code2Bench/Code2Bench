from typing import List

def _filter_invalid_triples(triples: List[List[str]]) -> List[List[str]]:
    # Convert each element to a string to ensure consistency
    cleaned_triples = [[str(element) for element in triple] for triple in triples]
    
    # Check if each triple has exactly three elements
    valid_triples = []
    for triple in cleaned_triples:
        if len(triple) != 3:
            continue
        # Check if all elements are strings or empty after stripping whitespace
        if all(isinstance(element, str) or (element.strip() != '') for element in triple):
            valid_triples.append(triple)
    
    # Remove duplicates
    unique_triples = []
    seen = set()
    for triple in valid_triples:
        if triple not in seen:
            seen.add(triple)
            unique_triples.append(triple)
    
    return unique_triples