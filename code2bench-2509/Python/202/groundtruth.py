from typing import List

from typing import List

def _parse_keywords_fallback(response: str) -> List[str]:
    keywords = []
    for line in response.strip().split("\n"):
        keyword = line.strip()
        keyword = keyword.lstrip("- *•").strip()
        if keyword and not keyword.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")):
            keyword = keyword.strip("\"'")
            if keyword:
                keywords.append(keyword)
    return keywords[:10]