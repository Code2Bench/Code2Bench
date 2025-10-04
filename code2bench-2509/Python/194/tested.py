from typing import Dict, Any, Optional

def _extract_publication_date(result: Dict[str, Any]) -> Optional[str]:
    # Check 'pagemap' for potential date fields
    if 'pagemap' in result:
        for key in ['date', 'pubdate', 'article:published_time']:
            if key in result['pagemap']:
                if isinstance(result['pagemap'][key], str):
                    return result['pagemap'][key]
    
    # Check 'metatags' for potential date fields
    if 'metatags' in result:
        for key in ['date', 'article:published_time']:
            if key in result['metatags']:
                if isinstance(result['metatags'][key], str):
                    return result['metatags'][key]
    
    # Check direct 'date' field
    if 'date' in result:
        if isinstance(result['date'], str):
            return result['date']
    
    return None