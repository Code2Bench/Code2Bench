from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import urllib.parse
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
def _is_url(policy_string: str) -> bool:
    """Check if the policy string is a URL."""
    try:
        parsed = urllib.parse.urlparse(policy_string)
        return parsed.scheme in ('http', 'https')
    except Exception:  # pylint: disable=broad-except
        return False

# Strategy for generating policy strings
def policy_string_strategy():
    # Generate valid URLs
    valid_url = st.builds(
        lambda scheme, netloc, path: f"{scheme}://{netloc}{path}",
        st.sampled_from(['http', 'https']),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P')), min_size=1, max_size=10),
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=0, max_size=10)
    )
    
    # Generate invalid URLs or random strings
    invalid_url = st.one_of(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20),
        st.builds(
            lambda scheme, netloc, path: f"{scheme}://{netloc}{path}",
            st.sampled_from(['ftp', 'file', 'mailto']),
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P')), min_size=1, max_size=10),
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=0, max_size=10)
        )
    )
    
    return st.one_of(valid_url, invalid_url)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(policy_string=policy_string_strategy())
@example(policy_string="http://example.com")
@example(policy_string="https://example.com/path")
@example(policy_string="ftp://example.com")
@example(policy_string="random string")
@example(policy_string="")
def test_is_url(policy_string: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    policy_string_copy = copy.deepcopy(policy_string)

    # Call func0 to verify input validity
    try:
        expected = _is_url(policy_string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "policy_string": policy_string_copy
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