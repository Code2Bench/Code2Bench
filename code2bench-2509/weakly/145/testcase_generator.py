from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import unicodedata
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
def decompose(path):
    if isinstance(path, str):
        return unicodedata.normalize('NFD', path)
    try:
        path = path.decode('utf-8')
        path = unicodedata.normalize('NFD', path)
        path = path.encode('utf-8')
    except UnicodeError:
        pass  # Not UTF-8
    return path

# Strategies for generating inputs
def path_strategy():
    return st.one_of(
        st.text(min_size=0, max_size=100),
        st.binary(min_size=0, max_size=100)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(path=path_strategy())
@example(path="")
@example(path="café")
@example(path="café".encode('utf-8'))
@example(path="café".encode('latin-1'))
@example(path="こんにちは")
@example(path="こんにちは".encode('utf-8'))
@example(path="こんにちは".encode('shift_jis'))
def test_decompose(path):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    path_copy = copy.deepcopy(path)

    # Call func0 to verify input validity
    try:
        expected = decompose(path_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    if isinstance(path_copy, bytes):
        path_copy = list(path_copy)
    generated_cases.append({
        "Inputs": {
            "path": path_copy
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