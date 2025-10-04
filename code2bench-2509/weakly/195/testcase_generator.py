from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from collections import Counter
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
def f1_score(prediction, ground_truth, **kwargs):
    common = Counter(prediction) & Counter(ground_truth)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction)
    recall = 1.0 * num_same / len(ground_truth)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1

# Strategies for generating inputs
def list_strategy():
    return st.lists(st.text(min_size=1, max_size=10), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    prediction=list_strategy(),
    ground_truth=list_strategy(),
    kwargs=st.fixed_dictionaries({})
)
@example(prediction=[], ground_truth=[], kwargs={})
@example(prediction=["a"], ground_truth=["a"], kwargs={})
@example(prediction=["a", "b"], ground_truth=["a", "b"], kwargs={})
@example(prediction=["a", "b"], ground_truth=["b", "c"], kwargs={})
@example(prediction=["a", "a", "b"], ground_truth=["a", "b", "b"], kwargs={})
@example(prediction=["a", "b", "c"], ground_truth=["d", "e", "f"], kwargs={})
def test_f1_score(prediction, ground_truth, kwargs):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    prediction_copy = copy.deepcopy(prediction)
    ground_truth_copy = copy.deepcopy(ground_truth)
    kwargs_copy = copy.deepcopy(kwargs)

    # Call func0 to verify input validity
    try:
        expected = f1_score(prediction_copy, ground_truth_copy, **kwargs_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "prediction": prediction_copy,
            "ground_truth": ground_truth_copy,
            "kwargs": kwargs_copy
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