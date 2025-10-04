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
def url_to_provider_name(url: str) -> str:
    """Create a sanitized provider name from a URL."""
    parsed_url = urlparse(url)
    # Combine host and path, remove leading slash from path
    name = parsed_url.netloc + parsed_url.path
    # Replace characters that are invalid for identifiers
    return name.replace('.', '_').replace('/', '_').replace('-', '_')

# Strategy for generating URLs
def url_strategy():
    # Generate valid URL components
    scheme = st.sampled_from(["http", "https"])
    netloc = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'),
        min_size=1, max_size=15
    )
    path = st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='/-'),
            min_size=1, max_size=10
        ),
        min_size=0, max_size=3
    ).map(lambda x: '/' + '/'.join(x))
    return st.builds(
        lambda s, n, p: f"{s}://{n}{p}",
        scheme, netloc, path
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="http://example.com")
@example(url="https://sub.domain.org/path/to/resource")
@example(url="http://example.com/")
@example(url="https://example.com/path_with-hyphens")
@example(url="http://example.com/path/with/slashes")
@example(url="https://example.com/path.with.dots")
def test_url_to_provider_name(url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_copy = copy.deepcopy(url)

    # Call func0 to verify input validity
    try:
        expected = url_to_provider_name(url_copy)
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