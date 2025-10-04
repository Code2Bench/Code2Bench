import re
from urllib.parse import urlparse

def find_github_issues(message: str) -> set:
    issue_pattern = re.compile(
        r'#(\d+)|'
        r'(https?:\/\/)?(www\.)?github\.com\/microsoft\/wsl\/issue\/(\d+)',
        re.IGNORECASE
    )
    matches = issue_pattern.findall(message)
    issues = set()
    for match in matches:
        if match[0]:  # Standalone issue number
            issues.add(f'#{match[0]}')
        elif match[3]:  # Issue URL
            issues.add(f'#{match[3]}')
    return issues