from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import bisect
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
def _get_padded_token_len(paddings: list[int], x: int) -> int:
    index = bisect.bisect_left(paddings, x)
    assert index < len(paddings)
    return paddings[index]

# Strategies for generating inputs
def paddings_strategy():
    return st.lists(
        st.integers(min_value=0, max_value=100),
        min_size=1,
        max_size=10,
        unique=True
    ).map(lambda lst: sorted(lst))

def x_strategy(paddings):
    return st.integers(min_value=0, max_value=paddings[-1] if paddings else 100)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    paddings=paddings_strategy(),
    x=st.builds(
        lambda p: x_strategy(p),
        paddings_strategy()
    )
)
@example(paddings=[0], x=0)
@example(paddings=[10, 20, 30], x=15)
@example(paddings=[5, 10, 15], x=5)
@example(paddings=[1, 2, 3, 4, 5], x=6)
def test_get_padded_token_len(paddings: list[int], x: int):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    paddings_copy = copy.deepcopy(paddings)
    x_copy = copy.deepcopy(x)

    # Call func0 to verify input validity
    try:
        expected = _get_padded_token_len(paddings_copy, x_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "paddings": paddings_copy,
            "x": x_copy
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