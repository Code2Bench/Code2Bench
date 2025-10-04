from typing import List, Dict

def group_sentences(corrected_srt: List[Dict[str, float]], threshold: float = 1.0) -> List[List[Dict[str, float]]]:
    groups = []
    current_group = []
    
    for sentence in corrected_srt:
        if not current_group:
            current_group.append(sentence)
        else:
            last_end = current_group[-1]['end']
            if sentence['start'] - last_end <= threshold:
                current_group.append(sentence)
            else:
                groups.append(current_group)
                current_group = [sentence]
    
    if current_group:
        groups.append(current_group)
    
    return groups