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
def _parse_url(base_url: str) -> tuple[str, str]:
    """Parse a base URL and return (host, port) as strings.

    This is more robust than simple string splitting and supports different schemes
    and URL shapes like trailing paths.
    """
    parsed = urlparse(base_url)
    return parsed.hostname or "127.0.0.1", (
        str(parsed.port) if parsed.port is not None else ""
    )

# Strategy for generating base URLs
def base_url_strategy():
    # Generate valid schemes
    scheme = st.sampled_from(["http", "https", "ftp", ""])
    
    # Generate hostnames
    hostname = st.one_of(
        st.just("127.0.0.1"),
        st.just("localhost"),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'), min_size=1, max_size=15)
    )
    
    # Generate ports
    port = st.one_of(
        st.just(""),
        st.integers(min_value=1, max_value=65535).map(str)
    )
    
    # Generate paths
    path = st.one_of(
        st.just(""),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
    )
    
    # Combine into URLs
    return st.builds(
        lambda s, h, p, pt: f"{s}://{h}:{p}/{pt}" if s and p else f"{s}://{h}/{pt}" if s else f"{h}:{p}/{pt}" if p else f"{h}/{pt}",
        scheme, hostname, port, path
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(base_url=base_url_strategy())
@example(base_url="http://localhost:8080")
@example(base_url="https://example.com")
@example(base_url="ftp://127.0.0.1")
@example(base_url="127.0.0.1:8080")
@example(base_url="localhost")
@example(base_url="")
def test_parse_url(base_url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    base_url_copy = copy.deepcopy(base_url)

    # Call func0 to verify input validity
    try:
        expected_host, expected_port = _parse_url(base_url_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "base_url": base_url_copy
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