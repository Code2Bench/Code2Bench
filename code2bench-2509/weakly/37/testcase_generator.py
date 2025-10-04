from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import base64
import re
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
def base64decode(s: str):
    """
    Decode base64 `str` to original `bytes`.
    If the input is not a valid base64 string, return None.

    Args:
        s(str): A base64 `str` that can be used in text file.

    Returns:
        Optional[bytes]: The original decoded data with type `bytes`.
            If the input is not a valid base64 string, return None.
    """
    _base64_regex = re.compile(r'^(?:[A-Za-z\d+/]{4})*(?:[A-Za-z\d+/]{3}=|[A-Za-z\d+/]{2}==)?$')
    s = s.translate(base64._urlsafe_decode_translation)
    if not _base64_regex.fullmatch(s):
        return None
    try:
        return base64.urlsafe_b64decode(s)
    except base64.binascii.Error:
        return None

# Strategy for generating base64 strings
def base64_strategy():
    # Generate valid base64 strings
    valid_base64 = st.from_regex(r'^(?:[A-Za-z\d+/]{4})*(?:[A-Za-z\d+/]{3}=|[A-Za-z\d+/]{2}==)?$', fullmatch=True)
    # Generate invalid base64 strings
    invalid_base64 = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    return st.one_of(valid_base64, invalid_base64)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s=base64_strategy())
@example(s="")
@example(s="aGVsbG8=")  # "hello"
@example(s="d29ybGQ=")  # "world"
@example(s="invalid_base64")
@example(s="aGVsbG8")  # Invalid (missing padding)
@example(s="aGVsbG8===")  # Invalid (extra padding)
def test_base64decode(s: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    s_copy = copy.deepcopy(s)

    # Call func0 to verify input validity
    try:
        expected = base64decode(s_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "s": s_copy
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