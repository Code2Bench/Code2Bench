import json
import copy
from datetime import datetime
from typing import Any
from helper import deep_compare, load_test_cases_from_json
from tested import transform_single_repo_commits_to_relationships as func1

# Ground truth function (func0), keep its original implementation and name
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

# Define compare_outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            repo_name = inputs["repo_name"]
            commits = inputs["commits"]
            organization = inputs["organization"]

            try:
                expected_output = transform_single_repo_commits_to_relationships(repo_name, commits, organization)
                actual_output = func1(repo_name, commits, organization)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output,
                        "actual": actual_output
                    })
            except Exception as e:
                failed_count += 1
                failures.append({
                    "case_id": i+1,
                    "type": "ExecutionError",
                    "inputs": inputs,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })

    except Exception as e:
        execution_error = {
            "type": "CriticalExecutionError",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }

    summary = {
        "passed": passed_count,
        "failed": failed_count,
        "total": len(test_cases),
        "failures": failures[:10],
        "execution_error": execution_error
    }

    print("\n---DIAGNOSTIC_SUMMARY_START---")
    print(json.dumps(summary, indent=2))
    print("---DIAGNOSTIC_SUMMARY_END---")

# Main block
if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    if not test_cases:
        print("No test cases found.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)