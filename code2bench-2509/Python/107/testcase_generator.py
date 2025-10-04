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
def validate_and_extract_os_classifiers(classifiers: list) -> list:
    os_classifiers = [c for c in classifiers if c.startswith("Operating System :: ")]
    if not os_classifiers:
        return []

    os_values = [c[len("Operating System :: ") :] for c in os_classifiers]
    valid_os_prefixes = {"Microsoft", "POSIX", "MacOS", "OS Independent"}

    for os_value in os_values:
        if not any(os_value.startswith(prefix) for prefix in valid_os_prefixes):
            return []

    return os_values

# Strategy for generating classifiers
def classifier_strategy():
    valid_prefixes = ["Operating System :: Microsoft", "Operating System :: POSIX", "Operating System :: MacOS", "Operating System :: OS Independent"]
    invalid_prefixes = ["Operating System :: Invalid", "Operating System :: Unknown"]
    return st.one_of([
        st.lists(st.one_of([st.from_regex(r"[a-zA-Z0-9 ]+")]), min_size=1, max_size=10),
        st.lists(st.one_of([st.sampled_from(valid_prefixes), st.sampled_from(invalid_prefixes)]), min_size=1, max_size=10),
        st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50), min_size=1, max_size=10)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(classifiers=classifier_strategy())
@example(classifiers=[])
@example(classifiers=["Operating System :: Microsoft Windows"])
@example(classifiers=["Operating System :: POSIX Linux"])
@example(classifiers=["Operating System :: MacOS Catalina"])
@example(classifiers=["Operating System :: OS Independent"])
@example(classifiers=["Operating System :: Invalid OS"])
@example(classifiers=["Operating System :: Microsoft Windows", "Operating System :: POSIX Linux"])
@example(classifiers=["Operating System :: Microsoft Windows", "Operating System :: Invalid OS"])
def test_validate_and_extract_os_classifiers(classifiers):
    global stop_collecting
    if stop_collecting:
        return
    
    classifiers_copy = copy.deepcopy(classifiers)
    try:
        expected = validate_and_extract_os_classifiers(classifiers_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(c.startswith("Operating System :: ") for c in classifiers):
        generated_cases.append({
            "Inputs": {"classifiers": classifiers},
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