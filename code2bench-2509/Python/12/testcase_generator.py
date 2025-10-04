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
def build_expected_version_hex(matches):
    patch_level_serial = matches["PATCH"]
    serial = None
    try:
        major = int(matches["MAJOR"])
        minor = int(matches["MINOR"])
        flds = patch_level_serial.split(".")
        if flds:
            patch = int(flds[0])
            level = None
            if len(flds) == 1:
                level = "0"
                serial = 0
            elif len(flds) == 2:
                level_serial = flds[1]
                for level in ("a", "b", "c", "dev"):
                    if level_serial.startswith(level):
                        serial = int(level_serial[len(level) :])
                        break
    except ValueError:
        pass
    if serial is None:
        msg = 'Invalid PYBIND11_VERSION_PATCH: "{}"'.format(patch_level_serial)
        raise RuntimeError(msg)
    return (
        "0x"
        + "{:02x}{:02x}{:02x}{}{:x}".format(
            major, minor, patch, level[:1], serial
        ).upper()
    )

# Strategy for generating valid patch level serial strings
def patch_level_serial_strategy():
    return st.one_of([
        st.tuples(
            st.integers(min_value=0, max_value=99),
            st.just("")
        ).map(lambda x: f"{x[0]}"),
        st.tuples(
            st.integers(min_value=0, max_value=99),
            st.sampled_from(["a", "b", "c", "dev"]),
            st.integers(min_value=0, max_value=99)
        ).map(lambda x: f"{x[0]}.{x[1]}{x[2]}")
    ])

# Strategy for generating matches dictionary
def matches_strategy():
    return st.fixed_dictionaries({
        "MAJOR": st.integers(min_value=0, max_value=99),
        "MINOR": st.integers(min_value=0, max_value=99),
        "PATCH": patch_level_serial_strategy()
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(matches=matches_strategy())
@example(matches={"MAJOR": 1, "MINOR": 2, "PATCH": "3"})
@example(matches={"MAJOR": 4, "MINOR": 5, "PATCH": "6.a7"})
@example(matches={"MAJOR": 8, "MINOR": 9, "PATCH": "10.b11"})
@example(matches={"MAJOR": 12, "MINOR": 13, "PATCH": "14.c15"})
@example(matches={"MAJOR": 16, "MINOR": 17, "PATCH": "18.dev19"})
def test_build_expected_version_hex(matches):
    global stop_collecting
    if stop_collecting:
        return
    
    matches_copy = copy.deepcopy(matches)
    try:
        expected = build_expected_version_hex(matches_copy)
    except RuntimeError:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"matches": matches},
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