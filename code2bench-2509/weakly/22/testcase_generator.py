from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def validate_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False

    try:
        result = urlparse(url)
        return all([
            result.scheme in ['http', 'https'],
            result.netloc,
            len(url) < 2048  # URL长度限制
        ])
    except Exception:
        return False

# Strategy for generating URLs
def url_strategy():
    # Generate valid schemes
    scheme = st.sampled_from(['http', 'https'])
    
    # Generate valid netloc (domain and port)
    domain = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'),
        min_size=1, max_size=63
    )
    port = st.integers(min_value=0, max_value=65535).map(lambda x: f":{x}" if x != 0 else "")
    netloc = st.builds(lambda d, p: f"{d}{p}", domain, port)
    
    # Generate path, query, and fragment
    path = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S'), whitelist_characters='/'),
        min_size=0, max_size=100
    )
    query = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S'), whitelist_characters='=&?'),
        min_size=0, max_size=100
    )
    fragment = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S'), whitelist_characters='#'),
        min_size=0, max_size=100
    )
    
    # Combine into a URL
    return st.builds(
        lambda s, n, p, q, f: f"{s}://{n}{p}?{q}#{f}",
        scheme, netloc, path, query, fragment
    ).filter(lambda x: len(x) < 2048)  # Filter URLs that exceed length limit

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="")
@example(url="http://example.com")
@example(url="https://example.com:8080/path?query=value#fragment")
@example(url="ftp://invalid.com")  # Invalid scheme
@example(url="http://")  # Missing netloc
@example(url="http://example.com/" + "a" * 2048)  # Exceeds length limit
def test_validate_url(url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_copy = copy.deepcopy(url)

    # Call func0 to verify input validity
    try:
        expected = validate_url(url_copy)
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