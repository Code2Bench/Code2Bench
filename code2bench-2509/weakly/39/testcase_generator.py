from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from urllib.parse import urlparse, urlunparse
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
def is_url(path: str) -> bool:
    """URL detection."""
    result = urlparse(path)
    # Both scheme and netloc must be present for a valid URL
    return all([result.scheme, result.netloc])

# Strategy for generating URLs and non-URL strings
def path_strategy():
    # Generate valid URLs
    scheme = st.sampled_from(["http", "https", "ftp", "sftp"])
    netloc = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'), min_size=1, max_size=20)
    path = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
    valid_url = st.builds(
        lambda s, n, p: f"{s}://{n}/{p}",
        scheme, netloc, path
    )
    
    # Generate invalid URLs (missing scheme or netloc)
    invalid_url = st.one_of(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.builds(lambda s, p: f"{s}://{p}", scheme, path),
        st.builds(lambda n, p: f"{n}/{p}", netloc, path)
    )
    
    return st.one_of(valid_url, invalid_url)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(path=path_strategy())
@example(path="http://example.com")
@example(path="https://sub.domain.org/path/to/resource")
@example(path="ftp://user@host/path")
@example(path="invalid.url")
@example(path="missing.scheme.com/path")
@example(path="http://")
@example(path="://missing.netloc")
def test_is_url(path: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    path_copy = copy.deepcopy(path)

    # Call func0 to verify input validity
    try:
        expected = is_url(path_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "path": path_copy
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