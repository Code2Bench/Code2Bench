from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from datetime import datetime
from typing import Any
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def transform_single_repo_commits_to_relationships(
    repo_name: str,
    commits: list[dict[str, Any]],
    organization: str,
) -> list[dict[str, Any]]:
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

# Strategies for generating inputs
def repo_name_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'), min_size=1, max_size=20)

def organization_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'), min_size=1, max_size=20)

def commit_strategy():
    return st.fixed_dictionaries({
        "author": st.one_of(
            st.none(),
            st.fixed_dictionaries({
                "user": st.one_of(
                    st.none(),
                    st.fixed_dictionaries({
                        "url": st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters=':/._-'), min_size=1, max_size=50)
                    })
                )
            })
        ),
        "committedDate": st.datetimes().map(lambda dt: dt.isoformat() + "Z")
    })

def commits_strategy():
    return st.lists(commit_strategy(), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    repo_name=repo_name_strategy(),
    commits=commits_strategy(),
    organization=organization_strategy()
)
@example(
    repo_name="repo1",
    commits=[],
    organization="org1"
)
@example(
    repo_name="repo2",
    commits=[{"author": None, "committedDate": "2023-01-01T00:00:00Z"}],
    organization="org2"
)
@example(
    repo_name="repo3",
    commits=[{"author": {"user": {"url": "https://github.com/user1"}}, "committedDate": "2023-01-01T00:00:00Z"}],
    organization="org3"
)
@example(
    repo_name="repo4",
    commits=[
        {"author": {"user": {"url": "https://github.com/user1"}}, "committedDate": "2023-01-01T00:00:00Z"},
        {"author": {"user": {"url": "https://github.com/user2"}}, "committedDate": "2023-01-02T00:00:00Z"}
    ],
    organization="org4"
)
def test_transform_single_repo_commits_to_relationships(repo_name: str, commits: list[dict[str, Any]], organization: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    repo_name_copy = copy.deepcopy(repo_name)
    commits_copy = copy.deepcopy(commits)
    organization_copy = copy.deepcopy(organization)

    # Call func0 to verify input validity
    try:
        expected = transform_single_repo_commits_to_relationships(repo_name_copy, commits_copy, organization_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "repo_name": repo_name_copy,
            "commits": commits_copy,
            "organization": organization_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)