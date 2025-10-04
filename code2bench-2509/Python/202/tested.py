from typing import List

def _parse_keywords_fallback(response: str) -> List[str]:
    keywords = []
    for line in response.splitlines():
        line = line.strip()
        if not line:
            continue
        # Remove leading dashes, asterisks, or bullet points
        if line.startswith('-') or line.startswith('*') or line.startswith('•'):
            line = line[1:]
        # Skip lines starting with numbered lists
        if line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.') or line.startswith('6.') or line.startswith('7.') or line.startswith('8.') or line.startswith('9.') or line.startswith('10.'):
            continue
        # Remove surrounding quotes
        if line.startswith('"') or line.endswith('"') or line.startswith("'") or line.endswith("'"):
            line = line[1:-1]
        # Add keyword if it's non-empty
        if line:
            keywords.append(line)
    return keywords[:10]