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
def check_resource_allowed(requested_resource: str, configured_resource: str) -> bool:
    """Check if a requested resource URL matches a configured resource URL."""
    requested = urlparse(requested_resource)
    configured = urlparse(configured_resource)

    if requested.scheme.lower() != configured.scheme.lower() or requested.netloc.lower() != configured.netloc.lower():
        return False

    requested_path = requested.path
    configured_path = configured.path

    if len(requested_path) < len(configured_path):
        return False

    if not requested_path.endswith("/"):
        requested_path += "/"
    if not configured_path.endswith("/"):
        configured_path += "/"

    return requested_path.startswith(configured_path)

# Strategies for generating URLs
def url_strategy():
    scheme = st.sampled_from(["http", "https"])
    netloc = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'), min_size=1, max_size=10)
    path = st.lists(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_'), min_size=1, max_size=5),
        min_size=0, max_size=5
    ).map(lambda parts: "/" + "/".join(parts))
    return st.builds(
        lambda s, n, p: f"{s}://{n}{p}",
        scheme, netloc, path
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    requested_resource=url_strategy(),
    configured_resource=url_strategy()
)
@example(
    requested_resource="http://example.com/api/",
    configured_resource="http://example.com/api/"
)
@example(
    requested_resource="http://example.com/api/v1",
    configured_resource="http://example.com/api/"
)
@example(
    requested_resource="http://example.com/api",
    configured_resource="http://example.com/api/"
)
@example(
    requested_resource="http://example.com/api123",
    configured_resource="http://example.com/api/"
)
@example(
    requested_resource="https://example.com/api/",
    configured_resource="http://example.com/api/"
)
@example(
    requested_resource="http://example.com:8080/api/",
    configured_resource="http://example.com/api/"
)
@example(
    requested_resource="http://example.com/api/",
    configured_resource="http://example.com/api/v1/"
)
def test_check_resource_allowed(requested_resource: str, configured_resource: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    requested_resource_copy = copy.deepcopy(requested_resource)
    configured_resource_copy = copy.deepcopy(configured_resource)

    # Call func0 to verify input validity
    try:
        expected = check_resource_allowed(requested_resource_copy, configured_resource_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "requested_resource": requested_resource_copy,
            "configured_resource": configured_resource_copy
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