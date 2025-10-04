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
def syndrome_booleans(syndrome, measurements):
    if syndrome[0] == 0:
        m = ~measurements[0]
    else:
        m = measurements[0]

    for i, elem in enumerate(syndrome[1:]):
        if elem == 0:
            m = m & ~measurements[i + 1]
        else:
            m = m & measurements[i + 1]

    return m

# Strategy for generating syndrome and measurements
def syndrome_measurements_strategy():
    return st.tuples(
        st.lists(st.booleans(), min_size=1, max_size=10),  # syndrome
        st.lists(st.booleans(), min_size=1, max_size=10)  # measurements
    ).filter(lambda x: len(x[0]) == len(x[1]))  # Ensure equal lengths

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(data=syndrome_measurements_strategy())
@example(data=([True], [True]))
@example(data=([False], [False]))
@example(data=([True, False], [True, False]))
@example(data=([False, True], [False, True]))
@example(data=([True, True, True], [True, True, True]))
@example(data=([False, False, False], [False, False, False]))
def test_syndrome_booleans(data):
    global stop_collecting
    if stop_collecting:
        return
    
    syndrome, measurements = data
    syndrome_copy = copy.deepcopy(syndrome)
    measurements_copy = copy.deepcopy(measurements)
    try:
        expected = syndrome_booleans(syndrome_copy, measurements_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"syndrome": syndrome, "measurements": measurements},
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