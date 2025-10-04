from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from base64 import urlsafe_b64decode

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def str_from_base64url(base64url: str) -> str:
    base64url_with_padding = base64url + "=" * (-len(base64url) % 4)
    return urlsafe_b64decode(base64url_with_padding).decode("utf-8")

# Strategy for generating base64url strings
def base64url_strategy():
    # Generate valid base64url characters
    return st.text(
        alphabet=st.characters(
            whitelist_categories=('L', 'N'),
            whitelist_characters='-_'
        ),
        min_size=0,
        max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(base64url=base64url_strategy())
@example(base64url="")
@example(base64url="YQ")
@example(base64url="YWI")
@example(base64url="YWJj")
@example(base64url="YWJjZA")
@example(base64url="YWJjZGU")
def test_str_from_base64url(base64url: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    base64url_copy = copy.deepcopy(base64url)

    # Call func0 to verify input validity
    try:
        expected = str_from_base64url(base64url_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "base64url": base64url_copy
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