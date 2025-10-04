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
def _ext_from_uri(uri: str) -> str:
    path = urlparse(uri).path
    if "." in path:
        return "." + path.split(".")[-1].lower()
    return ""

# Strategy for generating URIs
def uri_strategy():
    # Generate valid URIs with optional paths and extensions
    scheme = st.sampled_from(["http", "https", "ftp", "file"])
    netloc = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'), min_size=1, max_size=10)
    path = st.lists(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-_/'), min_size=1, max_size=5),
        min_size=0, max_size=3
    ).map(lambda x: "/" + "/".join(x))
    extension = st.one_of(
        st.just(""),
        st.sampled_from([".txt", ".jpg", ".png", ".pdf", ".html"])
    )
    return st.builds(
        lambda s, n, p, e: f"{s}://{n}{p}{e}",
        scheme, netloc, path, extension
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(uri=uri_strategy())
@example(uri="http://example.com")
@example(uri="https://example.com/index.html")
@example(uri="ftp://example.com/file.txt")
@example(uri="file:///path/to/file.pdf")
@example(uri="http://example.com/noextension")
@example(uri="https://example.com/path/to/file.jpg")
def test_ext_from_uri(uri: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    uri_copy = copy.deepcopy(uri)

    # Call func0 to verify input validity
    try:
        expected = _ext_from_uri(uri_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "uri": uri_copy
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