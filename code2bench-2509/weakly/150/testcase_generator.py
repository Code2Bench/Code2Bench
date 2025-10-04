from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
from urllib.parse import urlparse
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
def find_github_issues(message: str):
    # Look for urls first
    urls = [urlparse(e) for e in re.findall(r"https?://[^\s^\)]+", message)]

    issue_urls = [e for e in urls if e.hostname == 'github.com' and e.path.lower().startswith('/microsoft/wsl/issues/')]

    issues = set(['#' + e.path.split('/')[-1] for e in issue_urls])

    # Then add issue numbers
    for e in re.findall(r"#\d+", message):
        issues.add(e)

    return issues

# Strategy for generating message with potential URLs and issue numbers
def message_strategy():
    # Generate valid GitHub issue URLs
    github_issue_url = st.builds(
        lambda issue_num: f"https://github.com/microsoft/wsl/issues/{issue_num}",
        st.integers(min_value=1, max_value=9999)
    )
    
    # Generate other URLs
    other_url = st.builds(
        lambda domain, path: f"https://{domain}/{path}",
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'), min_size=1, max_size=10),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
    )
    
    # Generate issue numbers
    issue_number = st.builds(
        lambda num: f"#{num}",
        st.integers(min_value=1, max_value=9999)
    )
    
    # Mix URLs, issue numbers, and random text
    return st.lists(
        st.one_of(
            github_issue_url,
            other_url,
            issue_number,
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
        ),
        min_size=0, max_size=10
    ).map(lambda x: ' '.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(message=message_strategy())
@example(message="")
@example(message="https://github.com/microsoft/wsl/issues/123")
@example(message="#456")
@example(message="https://github.com/microsoft/wsl/issues/123 #456")
@example(message="https://example.com/not-an-issue")
@example(message="random text without issues")
def test_find_github_issues(message: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    message_copy = copy.deepcopy(message)

    # Call func0 to verify input validity
    try:
        expected = find_github_issues(message_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "message": message_copy
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