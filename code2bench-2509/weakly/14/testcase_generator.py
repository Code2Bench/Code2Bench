from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import itertools
import json
import os
import atexit
import copy
from typing import List, Tuple

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _pad_version(left: List[str], right: List[str]) -> Tuple[List[str], List[str]]:
    left_split, right_split = [], []

    # Get the release segment of our versions
    left_split.append(list(itertools.takewhile(lambda x: x.isdigit(), left)))
    right_split.append(list(itertools.takewhile(lambda x: x.isdigit(), right)))

    # Get the rest of our versions
    left_split.append(left[len(left_split[0]) :])
    right_split.append(right[len(right_split[0]) :])

    # Insert our padding
    left_split.insert(1, ["0"] * max(0, len(right_split[0]) - len(left_split[0])))
    right_split.insert(1, ["0"] * max(0, len(left_split[0]) - len(right_split[0])))

    return (
        list(itertools.chain.from_iterable(left_split)),
        list(itertools.chain.from_iterable(right_split)),
    )

# Strategies for generating inputs
def version_strategy():
    return st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N'), min_codepoint=33, max_codepoint=126),
            min_size=1,
            max_size=5
        ),
        min_size=1,
        max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    left=version_strategy(),
    right=version_strategy()
)
@example(left=["1", "0", "2"], right=["1", "0", "1"])
@example(left=["1", "a", "2"], right=["1", "b", "3"])
@example(left=["1"], right=["1", "0", "0"])
@example(left=["1", "0", "0"], right=["1"])
@example(left=[], right=[])  # Empty lists
@example(left=["1", "2", "3"], right=["a", "b", "c"])  # No digits
def test_pad_version(left: List[str], right: List[str]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    left_copy = copy.deepcopy(left)
    right_copy = copy.deepcopy(right)

    # Call func0 to verify input validity
    try:
        padded_left, padded_right = _pad_version(left_copy, right_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "left": left_copy,
            "right": right_copy
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