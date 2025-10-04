from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from urllib.parse import urlparse

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def get_url_root(url: str) -> str:
    supported_list = ["omniverse", "http", "https"]
    protocol = urlparse(url).scheme
    if protocol not in supported_list:
        raise RuntimeError("Unable to find root for {}".format(url))
        return ""
    server = f"{protocol}://{urlparse(url).netloc}"
    return server

# Strategy for generating URLs
def url_strategy():
    protocols = st.sampled_from(["omniverse", "http", "https"])
    domains = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'),
        min_size=1, max_size=15
    )
    paths = st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_'),
            min_size=1, max_size=10
        ),
        min_size=0, max_size=3
    ).map(lambda x: '/' + '/'.join(x))
    return st.builds(
        lambda p, d, path: f"{p}://{d}{path}",
        protocols, domains, paths
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="omniverse://example.com")
@example(url="http://example.com")
@example(url="https://example.com")
@example(url="ftp://example.com")
@example(url="omniverse://example.com/path/to/resource")
@example(url="http://example.com/path/to/resource")
@example(url="https://example.com/path/to/resource")
def test_get_url_root(url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_copy = copy.deepcopy(url)

    # Call func0 to verify input validity
    try:
        expected = get_url_root(url_copy)
    except RuntimeError:
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