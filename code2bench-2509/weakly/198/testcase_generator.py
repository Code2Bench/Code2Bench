from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import math
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
def total_byte_entropy_stats(python_code):
    # Count the occurrence of each byte (character for simplicity)
    byte_counts = {}
    for byte in python_code.encode('utf-8'):
        byte_counts[byte] = byte_counts.get(byte, 0) + 1

    total_bytes = sum(byte_counts.values())
    entropy = -sum(
        (count / total_bytes) * math.log2(count / total_bytes)
        for count in byte_counts.values()
    )

    return {'total_byte_entropy': entropy}

# Strategy for generating Python code strings
def python_code_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=0, max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(python_code=python_code_strategy())
@example(python_code="")
@example(python_code="a")
@example(python_code="abc")
@example(python_code="a" * 100)
@example(python_code="import math\nprint(math.pi)")
def test_total_byte_entropy_stats(python_code: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    python_code_copy = copy.deepcopy(python_code)

    # Call func0 to verify input validity
    try:
        expected = total_byte_entropy_stats(python_code_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "python_code": python_code_copy
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