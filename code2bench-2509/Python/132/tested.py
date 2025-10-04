from typing import List

def extract_context_factors(user_query: str) -> List[str]:
    # Convert the query to lowercase for case-insensitive search
    user_query_lower = user_query.lower()
    
    # Define the keyword mappings
    keyword_to_factor = {
        "technology": "tech",
        "complexity": "complex",
        "advanced": "advanced",
        "moderate": "moderate",
        "basic": "basic",
        "high": "high",
        "low": "low",
        "simple": "simple",
        "complex": "complex",
        "advanced": "advanced",
        "intermediate": "intermediate"
    }
    
    # Extract context factors from the query
    context_factors = []
    for keyword, factor in keyword_to_factor.items():
        if keyword in user_query_lower:
            context_factors.append(factor)
    
    return context_factors