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
def digit_version(version_str):
    digit_version = []
    for x in version_str.split('.'):
        if x.isdigit():
            digit_version.append(int(x))
        elif x.find('rc') != -1:
            patch_version = x.split('rc')
            digit_version.append(int(patch_version[0]) - 1)
            digit_version.append(int(patch_version[1]))
    return digit_version

# Strategy for generating version strings
def version_strategy():
    return st.one_of([
        st.lists(
            st.one_of([
                st.integers(min_value=0, max_value=999),
                st.tuples(st.integers(min_value=0, max_value=999), st.just("rc"), st.integers(min_value=0, max_value=999))
            ]),
            min_size=1,
            max_size=5
        ).map(lambda parts: ".".join(str(part) if isinstance(part, int) else f"{part[0]}{part[1]}{part[2]}" for part in parts)),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P')), min_size=1, max_size=20)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(version_str=version_strategy())
@example(version_str="1.2.3")
@example(version_str="1.2.3rc4")
@example(version_str="1.2.3.4.5")
@example(version_str="1.2.3rc4.5rc6")
@example(version_str="1.2.3.4rc5")
@example(version_str="1rc2")
@example(version_str="1.2.3.4.5rc6")
def test_digit_version(version_str):
    global stop_collecting
    if stop_collecting:
        return
    
    version_str_copy = copy.deepcopy(version_str)
    try:
        expected = digit_version(version_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(part.find('rc') != -1 for part in version_str.split('.')) or all(part.isdigit() for part in version_str.split('.')):
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