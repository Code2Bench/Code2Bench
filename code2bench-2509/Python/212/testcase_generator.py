from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def prepare_value(value):
    """Convert JSON list to list of selected values."""
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # Handle legacy comma-separated string format
        return [day.strip().lower() for day in value.split(",") if day.strip()]
    return value

# Strategy for generating inputs
value_strategy = st.one_of([
    st.none(),
    st.just(""),
    st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1), min_size=1, max_size=5),
    st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1).map(lambda s: ",".join([s[:i] for i in range(1, len(s))])),
    st.integers(),
    st.floats(allow_nan=False, allow_infinity=False),
    st.booleans()
])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(value=value_strategy)
@example(value=None)
@example(value="")
@example(value="a,b,c")
@example(value="a, b, c")
@example(value=["a", "b", "c"])
@example(value=42)
@example(value=True)
def test_prepare_value(value):
    global stop_collecting
    if stop_collecting:
        return
    
    value_copy = copy.deepcopy(value)
    try:
        expected = prepare_value(value_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(value, (str, list)) or value is None or value == "":
        generated_cases.append({
            "Inputs": {"value": value},
            "Expected": expected
        })
        if len(generated_cases) >= 500:
            stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)