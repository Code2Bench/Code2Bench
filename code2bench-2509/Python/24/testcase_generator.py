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
def parse_version_info(version_str):
    version_info = []
    for x in version_str.split('.'):
        if x.isdigit():
            version_info.append(int(x))
        elif x.find('rc') != -1:
            patch_version = x.split('rc')
            version_info.append(int(patch_version[0]))
            version_info.append(f'rc{patch_version[1]}')
    return tuple(version_info)

# Strategy for generating version strings
def version_strategy():
    return st.one_of([
        st.lists(st.integers(min_value=0, max_value=999), min_size=1, max_size=4).map(lambda x: '.'.join(map(str, x))),
        st.lists(st.one_of([
            st.integers(min_value=0, max_value=999),
            st.tuples(st.integers(min_value=0, max_value=999), st.integers(min_value=0, max_value=999)).map(lambda x: f"{x[0]}rc{x[1]}")
        ]), min_size=1, max_size=4).map(lambda x: '.'.join(map(str, x)))
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(version_str=version_strategy())
@example(version_str="1.2.3")
@example(version_str="1.2.3rc4")
@example(version_str="1.2.3.4")
@example(version_str="1.2.3.4rc5")
@example(version_str="1")
@example(version_str="1rc2")
def test_parse_version_info(version_str):
    global stop_collecting
    if stop_collecting:
        return
    
    version_str_copy = copy.deepcopy(version_str)
    try:
        expected = parse_version_info(version_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(x.isdigit() or 'rc' in x for x in version_str.split('.')):
        generated_cases.append({
            "Inputs": {"version_str": version_str},
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