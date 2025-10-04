from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import struct
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
def _formatinfo(format):
    size = struct.calcsize(format)
    return size, len(struct.unpack(format, b"\x00" * size))

# Strategy for generating format strings
def format_strategy():
    # Generate valid format strings based on struct module's format characters
    format_chars = st.sampled_from(['x', 'c', 'b', 'B', '?', 'h', 'H', 'i', 'I', 'l', 'L', 'q', 'Q', 'n', 'N', 'f', 'd', 's', 'p', 'P'])
    return st.lists(format_chars, min_size=1, max_size=10).map(lambda x: ''.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(format=format_strategy())
@example(format="i")
@example(format="f")
@example(format="d")
@example(format="c")
@example(format="b")
@example(format="B")
@example(format="?")
@example(format="h")
@example(format="H")
@example(format="l")
@example(format="L")
@example(format="q")
@example(format="Q")
@example(format="n")
@example(format="N")
@example(format="s")
@example(format="p")
@example(format="P")
@example(format="x")
def test_formatinfo(format: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    format_copy = copy.deepcopy(format)

    # Call func0 to verify input validity
    try:
        size, num_items = _formatinfo(format_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
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