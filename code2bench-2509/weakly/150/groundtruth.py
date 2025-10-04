
import re
from urllib.parse import urlparse

import re
from urllib.parse import urlparse

def find_github_issues(message: str):
    # Look for urls first
    urls = [urlparse(e) for e in re.findall(r"https?://[^\s^\)]+", message)]

    issue_urls = [e for e in urls if e.hostname == 'github.com' and e.path.lower().startswith('/microsoft/wsl/issues/')]

    issues = set(['#' + e.path.split('/')[-1] for e in issue_urls])

    # Then add issue numbers
    for e in re.findall(r"#\d+", message):
        issues.add(e)

    return issues