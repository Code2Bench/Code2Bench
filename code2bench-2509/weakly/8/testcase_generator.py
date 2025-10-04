from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Tuple
from collections import Counter

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def compute_token_overlap(prediction: str, reference: str) -> Tuple[int, int, int]:
    prediction_tokens = prediction.split()
    reference_tokens = reference.split()

    common = Counter(prediction_tokens) & Counter(reference_tokens)
    num_same = sum(common.values())

    return num_same, len(prediction_tokens), len(reference_tokens)

# Strategies for generating inputs
def text_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'Z'), min_codepoint=32, max_codepoint=126), min_size=0, max_size=50)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(prediction=text_strategy(), reference=text_strategy())
@example(prediction="", reference="")
@example(prediction="hello world", reference="world hello")
@example(prediction="hello", reference="hello")
@example(prediction="a b c", reference="d e f")
@example(prediction="a a a", reference="a a b")
@example(prediction="a b c", reference="a b c d e f")
def test_compute_token_overlap(prediction: str, reference: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    prediction_copy = copy.deepcopy(prediction)
    reference_copy = copy.deepcopy(reference)

    # Call func0 to verify input validity
    try:
        expected = compute_token_overlap(prediction_copy, reference_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "prediction": prediction_copy,
            "reference": reference_copy
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