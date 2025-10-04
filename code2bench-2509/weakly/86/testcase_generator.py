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
def _split_url(url: str) -> tuple[str, str]:
    parsed_url = urlparse(url)
    if not (parsed_url.scheme and parsed_url.netloc):
        raise ValueError(f"URL must include protocol and host name: {url}")
    return parsed_url.scheme.lower(), parsed_url.netloc.lower()

# Strategy for generating valid URLs
def url_strategy():
    # Generate valid schemes (e.g., http, https, ftp)
    scheme = st.sampled_from(["http", "https", "ftp", "sftp"])
    
    # Generate valid netloc (e.g., example.com, sub.domain.org)
    netloc = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.-'),
        min_size=1, max_size=20
    )
    
    # Generate domain suffix (e.g., com, org, net, edu)
    domain_suffix = st.sampled_from(['com', 'org', 'net', 'edu'])
    
    # Combine netloc and domain suffix into a valid domain
    domain = st.builds(
        lambda n, d: f"{n}.{d}",
        netloc, domain_suffix
    )
    
    # Combine scheme and domain into a valid URL
    return st.builds(
        lambda s, d: f"{s}://{d}",
        scheme, domain
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(url=url_strategy())
@example(url="http://example.com")
@example(url="https://sub.domain.org")
@example(url="ftp://ftp.example.net")
@example(url="sftp://sftp.example.edu")
def test_split_url(url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    url_copy = copy.deepcopy(url)

    # Call func0 to verify input validity
    try:
        scheme, netloc = _split_url(url_copy)
    except ValueError:
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