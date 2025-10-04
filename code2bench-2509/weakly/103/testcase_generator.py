from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import urllib
import json
import os
import atexit
import copy
from typing import Dict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def extract_url_params_to_dict(url: str) -> Dict:
    """Extract URL parameters to dict"""
    url_params_dict = dict()
    if not url:
        return url_params_dict
    parsed_url = urllib.parse.urlparse(url)
    url_params_dict = dict(urllib.parse.parse_qsl(parsed_url.query))
    return url_params_dict

# Strategy for generating URLs with potential parameters
def url_strategy():
    # Generate valid URL components
    scheme = st.sampled_from(["http", "https"])
    netloc = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'), min_size=1, max_size=20)
    path = st.lists(st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='/-'), min_size=1, max_size=10), min_size=0, max_size=5).map(lambda x: '/'.join(x))
    query = st.lists(
        st.tuples(
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'), min_size=1, max_size=10),
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'), min_size=0, max_size=10)
        ),
        min_size=0, max_size=5
    ).map(lambda x: '&'.join([f"{k}={v}" for k, v in x]))
    fragment = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'), min_size=0, max_size=10)
    
    return st.builds(
        lambda s, n, p, q, f: f"{s}://{n}/{p}?{q}#{f}",
        scheme, netloc, path, query, fragment
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="")
@example(url="http://example.com")
@example(url="https://example.com/path?param1=value1&param2=value2")
@example(url="http://example.com?param1=value1")
@example(url="https://example.com#fragment")
@example(url="http://example.com/path?param1=value1&param2=value2#fragment")
def test_extract_url_params_to_dict(url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_copy = copy.deepcopy(url)

    # Call func0 to verify input validity
    try:
        expected = extract_url_params_to_dict(url_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "url": url_copy
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