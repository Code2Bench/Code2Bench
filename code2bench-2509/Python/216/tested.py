from typing import List

def _format_community_content(base_text: str, entities: List[str], keywords: List[str]) -> str:
    result = base_text
    
    if entities:
        entities_str = ", ".join(entities[:3]) + " and " + str(len(entities) - 3) + " more" if len(entities) > 3 else ", ".join(entities)
        result += "\n  Contains:\n    Entities: " + entities_str
    
    if keywords:
        keywords_str = ", ".join(keywords[:3]) + " and " + str(len(keywords) - 3) + " more" if len(keywords) > 3 else ", ".join(keywords)
        result += "\n  Contains:\n    Keywords: " + keywords_str
    
    return result