from datetime import datetime
from typing import Any, List, Dict

def transform_single_repo_commits_to_relationships(
    repo_name: str,
    commits: List[Dict[str, Any]],
    organization: str,
) -> List[Dict[str, Any]]:
    relationships = []
    user_urls = set()
    commit_count = 0
    first_commit_date = None
    last_commit_date = None

    for commit in commits:
        author = commit.get("author")
        if not author:
            continue
        user_url = author.get("user", {}).get("url")
        if not user_url:
            continue

        user_urls.add(user_url)
        commit_count += 1
        commit_date = commit.get("commit", {}).get("author", {}).get("date")
        if commit_date:
            try:
                commit_date_obj = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")
                if not first_commit_date or commit_date_obj < first_commit_date:
                    first_commit_date = commit_date_obj
                if not last_commit_date or commit_date_obj > last_commit_date:
                    last_commit_date = commit_date_obj
            except ValueError:
                pass

    for user_url in user_urls:
        repo_url = f"https://github.com/{organization}/{repo_name}"
        relationships.append({
            "user_url": user_url,
            "repository_url": repo_url,
            "commit_count": commit_count,
            "first_commit_date": first_commit_date.isoformat() if first_commit_date else None,
            "last_commit_date": last_commit_date.isoformat() if last_commit_date else None
        })

    return relationships