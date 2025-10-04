from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import urllib
import base64
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
def _encode_auth(auth):
    auth_s = urllib.parse.unquote(auth)
    # convert to bytes
    auth_bytes = auth_s.encode()
    encoded_bytes = base64.b64encode(auth_bytes)
    # convert back to a string
    encoded = encoded_bytes.decode()
    # strip the trailing carriage return
    return encoded.replace('\n', '')

# Strategy for generating auth strings
def auth_strategy():
    # Generate valid URL-encoded strings with username and password
    username = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='._%+-'),
        min_size=1, max_size=10
    )
    password = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='._%+-'),
        min_size=1, max_size=10
    )
    return st.builds(
        lambda u, p: f"{u}%3A{p}",  # URL-encode the colon
        username, password
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(auth=auth_strategy())
@example(auth="username%3Apassword")
@example(auth="user%3Apass")
@example(auth="a%3Ab")
@example(auth="longuser%3A" + "longpass" * 10)
def test_encode_auth(auth: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    auth_copy = copy.deepcopy(auth)

    # Call func0 to verify input validity
    try:
        expected = _encode_auth(auth_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "auth": auth_copy
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