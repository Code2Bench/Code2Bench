from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import urllib.parse
import json
import os
import atexit
import copy
from typing import List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def modify_url(url: str, remove: List[str]) -> str:
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
    params = urllib.parse.parse_qs(query)
    for param_key in remove:
        if param_key in params:
            del params[param_key]
    query = urllib.parse.urlencode(params, doseq=True)
    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))

# Strategies for generating inputs
def url_strategy():
    return st.builds(
        lambda scheme, netloc, path, query, fragment: urllib.parse.urlunsplit((scheme, netloc, path, query, fragment)),
        scheme=st.sampled_from(["http", "https"]),
        netloc=st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        path=st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10),
        query=st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20),
        fragment=st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10)
    )

def remove_strategy():
    return st.lists(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        min_size=0, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy(), remove=remove_strategy())
@example(url="http://example.com", remove=[])
@example(url="http://example.com?param1=value1&param2=value2", remove=["param1"])
@example(url="https://example.com/path?param1=value1&param2=value2#fragment", remove=["param2"])
@example(url="http://example.com?param1=value1&param2=value2", remove=["param1", "param2"])
@example(url="http://example.com", remove=["nonexistent"])
def test_modify_url(url: str, remove: List[str]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    url_copy = copy.deepcopy(url)
    remove_copy = copy.deepcopy(remove)

    # Call func0 to verify input validity
    try:
        modified_url = modify_url(url_copy, remove_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "url": url_copy,
            "remove": remove_copy
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