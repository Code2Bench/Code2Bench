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
def linear_warmup_schedule(
    step: int,
    warmup_steps: int,
    start_value: float,
    end_value: float,
) -> float:
    if warmup_steps < 0:
        raise ValueError(f"Warmup steps {warmup_steps} can't be negative.")
    if step < 0:
        raise ValueError(f"Current step number {step} can't be negative.")
    if start_value < 0:
        raise ValueError(f"Start value {start_value} can't be negative.")
    if end_value <= 0:
        raise ValueError(f"End value {end_value} can't be non-positive.")
    if start_value > end_value:
        raise ValueError(
            f"Start value {start_value} must be less than or equal to end value {end_value}."
        )
    if step < warmup_steps:
        return start_value + step / warmup_steps * (end_value - start_value)
    else:
        return end_value

# Strategy for generating valid inputs
def valid_inputs_strategy():
    return st.tuples(
        st.integers(min_value=0, max_value=2147483647),  # step
        st.integers(min_value=0, max_value=2147483647),  # warmup_steps
        st.floats(min_value=0, allow_nan=False, allow_infinity=False),  # start_value
        st.floats(min_value=0, allow_nan=False, allow_infinity=False),  # end_value
    ).filter(lambda x: x[2] <= x[3])  # Ensure start_value <= end_value

# Strategy for generating invalid inputs
def invalid_inputs_strategy():
    return st.one_of([
        st.tuples(
            st.integers(min_value=-100, max_value=-1),  # step < 0
            st.integers(min_value=0, max_value=100),
            st.floats(min_value=0, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, allow_nan=False, allow_infinity=False),
        ),
        st.tuples(
            st.integers(min_value=0, max_value=100),
            st.integers(min_value=-100, max_value=-1),  # warmup_steps < 0
            st.floats(min_value=0, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, allow_nan=False, allow_infinity=False),
        ),
        st.tuples(
            st.integers(min_value=0, max_value=100),
            st.integers(min_value=0, max_value=100),
            st.floats(min_value=-100, max_value=-1),  # start_value < 0
            st.floats(min_value=0, allow_nan=False, allow_infinity=False),
        ),
        st.tuples(
            st.integers(min_value=0, max_value=100),
            st.integers(min_value=0, max_value=100),
            st.floats(min_value=0, allow_nan=False, allow_infinity=False),
            st.floats(min_value=-100, max_value=0),  # end_value <= 0
        ),
        st.tuples(
            st.integers(min_value=0, max_value=100),
            st.integers(min_value=0, max_value=100),
            st.floats(min_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=0.9),  # start_value > end_value
        ),
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(inputs=st.one_of([valid_inputs_strategy(), invalid_inputs_strategy()]))
@example((0, 0, 0.0, 0.0))
@example((10, 10, 0.0, 1.0))
@example((5, 10, 0.0, 1.0))
@example((15, 10, 0.0, 1.0))
@example((0, 10, 0.5, 1.0))
@example((10, 10, 0.5, 1.0))
@example((5, 10, 0.5, 1.0))
@example((15, 10, 0.5, 1.0))
def test_linear_warmup_schedule(inputs):
    global stop_collecting
    if stop_collecting:
        return
    
    step, warmup_steps, start_value, end_value = inputs
    inputs_copy = copy.deepcopy(inputs)
    try:
        expected = linear_warmup_schedule(step, warmup_steps, start_value, end_value)
    except ValueError:
        return  # Skip invalid inputs
    
    generated_cases.append({
        "Inputs": {
            "step": step,
            "warmup_steps": warmup_steps,
            "start_value": start_value,
            "end_value": end_value,
        },
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