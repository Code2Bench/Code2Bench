from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import binascii
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
def clean_pot(po_token: str):
    try:
        return base64.urlsafe_b64encode(
            base64.urlsafe_b64decode(urllib.parse.unquote(po_token))).decode()
    except (binascii.Error, ValueError):
        raise ValueError('Invalid PO Token')

# Strategy for generating PO tokens
def po_token_strategy():
    # Generate valid base64-encoded strings
    valid_base64 = st.binary(min_size=1, max_size=100).map(
        lambda x: base64.urlsafe_b64encode(x).decode()
    )
    
    # Generate invalid strings (e.g., non-base64 characters, malformed strings)
    invalid_base64 = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1, max_size=100
    )
    
    # Combine valid and invalid cases
    return st.one_of(valid_base64, invalid_base64)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(po_token=po_token_strategy())
@example(po_token="")
@example(po_token="aGVsbG8=")  # Valid base64
@example(po_token="aGVsbG8")  # Invalid base64 (missing padding)
@example(po_token="aGVsbG8=extra")  # Invalid base64 (extra characters)
@example(po_token="invalid!@#")  # Invalid base64 (non-base64 characters)
def test_clean_pot(po_token: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    po_token_copy = copy.deepcopy(po_token)

    # Call func0 to verify input validity
    try:
        expected = clean_pot(po_token_copy)
    except ValueError:
        pass  # Expected for invalid inputs
    except Exception:
        return  # Skip unexpected exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "po_token": po_token_copy
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