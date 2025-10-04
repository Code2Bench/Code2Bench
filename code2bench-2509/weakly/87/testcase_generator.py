from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from urllib.parse import urlunsplit, urlsplit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def metadata_url_for_resource(resource_url: str) -> str:
    """
    RFC 9728: insert '/.well-known/oauth-protected-resource' between host and path.
    If the resource has a path (e.g., '/mcp'), append it after the well-known suffix.
    """
    u = urlsplit(resource_url)
    path = u.path.lstrip("/")
    suffix = "/.well-known/oauth-protected-resource"
    if path:
        suffix += f"/{path}"
    return urlunsplit((u.scheme, u.netloc, suffix, "", ""))

# Strategy for generating resource URLs
def resource_url_strategy():
    scheme = st.sampled_from(["http", "https"])
    netloc = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'),
        min_size=1, max_size=20
    )
    path = st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_'),
            min_size=1, max_size=10
        ),
        min_size=0, max_size=3
    ).map(lambda x: "/" + "/".join(x) if x else "")
    return st.builds(
        lambda s, n, p: f"{s}://{n}{p}",
        scheme, netloc, path
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(resource_url=resource_url_strategy())
@example(resource_url="http://example.com")
@example(resource_url="https://example.com/path")
@example(resource_url="https://example.com/path/to/resource")
@example(resource_url="http://sub.domain.com")
@example(resource_url="https://sub.domain.com/path")
def test_metadata_url_for_resource(resource_url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    resource_url_copy = copy.deepcopy(resource_url)

    # Call func0 to verify input validity
    try:
        expected = metadata_url_for_resource(resource_url_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "resource_url": resource_url_copy
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