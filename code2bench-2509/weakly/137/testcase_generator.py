from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import base64
import json
import os
import atexit
import copy
from typing import Optional

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _serialize_bytes(o, format: Optional[str] = None) -> str:
    encoded = base64.b64encode(o).decode()
    if format == "base64url":
        return encoded.strip("=").replace("+", "-").replace("/", "_")
    return encoded

# Strategies for generating inputs
def bytes_strategy():
    return st.binary(min_size=0, max_size=100)

def format_strategy():
    return st.one_of(st.none(), st.just("base64url"))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    o=bytes_strategy(),
    format=format_strategy()
)
@example(o=b"", format=None)
@example(o=b"hello", format=None)
@example(o=b"world", format="base64url")
@example(o=b"12345", format="base64url")
@example(o=b"", format="base64url")
def test_serialize_bytes(o: bytes, format: Optional[str]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    o_copy = copy.deepcopy(o)
    format_copy = copy.deepcopy(format)

    # Call func0 to verify input validity
    try:
        expected = _serialize_bytes(o_copy, format_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "o": base64.b64encode(o_copy).decode(),  # Ensure JSON serializability
            "format": format_copy
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