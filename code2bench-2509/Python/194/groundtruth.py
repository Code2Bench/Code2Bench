from typing import Any, Dict, Optional

from typing import Dict, Any, Optional

def _extract_publication_date(result: Dict[str, Any]) -> Optional[str]:
    # Check for various date fields
    date_fields = ["pagemap", "metatags", "date"]

    for field in date_fields:
        if field in result:
            date_value = result[field]
            if isinstance(date_value, dict):
                # Look for common date keys
                for date_key in ["date", "pubdate", "article:published_time"]:
                    if date_key in date_value:
                        return date_value[date_key]
            elif isinstance(date_value, str):
                return date_value

    return None