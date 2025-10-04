from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from datetime import datetime
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
def ds_format(ds: str, input_format: str, output_format: str) -> str:
    return datetime.strptime(str(ds), input_format).strftime(output_format)

# Strategies for generating inputs
def ds_strategy():
    return st.datetimes(
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31)
    ).map(lambda dt: dt.strftime("%Y-%m-%d"))

def input_format_strategy():
    return st.sampled_from(["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"])

def output_format_strategy():
    return st.sampled_from(["%Y-%m-%d", "%m-%d-%y", "%d/%m/%Y", "%A %d %B %Y"])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    ds=ds_strategy(),
    input_format=input_format_strategy(),
    output_format=output_format_strategy()
)
@example(
    ds="2015-01-01",
    input_format="%Y-%m-%d",
    output_format="%m-%d-%y"
)
@example(
    ds="1/5/2015",
    input_format="%m/%d/%Y",
    output_format="%Y-%m-%d"
)
@example(
    ds="12/07/2024",
    input_format="%d/%m/%Y",
    output_format="%A %d %B %Y"
)
def test_ds_format(ds: str, input_format: str, output_format: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    ds_copy = copy.deepcopy(ds)
    input_format_copy = copy.deepcopy(input_format)
    output_format_copy = copy.deepcopy(output_format)

    # Call func0 to verify input validity
    try:
        expected = ds_format(ds_copy, input_format_copy, output_format_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "ds": ds_copy,
            "input_format": input_format_copy,
            "output_format": output_format_copy
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