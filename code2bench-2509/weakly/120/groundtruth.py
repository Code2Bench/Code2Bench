from typing import Any
from datetime import datetime

def transform_single_repo_commits_to_relationships(
    repo_name: str,
    commits: list[dict[str, Any]],
    organization: str,
) -> list[dict[str, Any]]:
    """
    Transform commits from a single repository into user-repository relationships.
    Optimized for memory efficiency by processing one repo at a time.

    :param repo_name: The repository name.
    :param commits: List of commit data from the repository.
    :param organization: The Github organization name.
    :return: List of user-repository relationship records for this repo.
    """
    if not commits:
        return []

    repo_url = f"https://github.com/{organization}/{repo_name}"

    # Count commits and track date ranges per user for this repo
    user_commit_data: dict[str, dict[str, Any]] = {}

    for commit in commits:
        # Get user URL from author, skip if not available
        author_user = commit.get("author", {}).get("user")
        if not author_user or not author_user.get("url"):
            continue

        user_url = author_user["url"]
        commit_date = datetime.fromisoformat(
            commit["committedDate"].replace("Z", "+00:00")
        )

        if user_url not in user_commit_data:
            user_commit_data[user_url] = {"commit_count": 0, "commit_dates": []}

        user_commit_data[user_url]["commit_count"] += 1
        user_commit_data[user_url]["commit_dates"].append(commit_date)

    # Transform to relationship records
    relationships = []
    for user_url, data in user_commit_data.items():
        commit_dates = data["commit_dates"]
        relationships.append(
            {
                "user_url": user_url,
                "repo_url": repo_url,
                "commit_count": data["commit_count"],
                "last_commit_date": max(commit_dates).isoformat(),
                "first_commit_date": min(commit_dates).isoformat(),
            }
        )

    return relationships