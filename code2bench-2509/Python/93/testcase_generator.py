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
def remove_mnemonic_marker(label: str) -> str:
    """Remove existing accelerator markers (&) from a label."""
    result = ""
    skip = False
    for i, ch in enumerate(label):
        if skip:
            skip = False
            continue
        if ch == "&":
            # escaped ampersand "&&"
            if i + 1 < len(label) and label[i + 1] == "&":
                result += "&&"
                skip = True
            # otherwise skip this '&'
            continue
        result += ch
    return result

# Strategy for generating labels with and without mnemonic markers
def label_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=0,
        max_size=50
    ).map(lambda s: s.replace("&", "&&"))  # Ensure valid mnemonic markers

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(label=label_strategy())
@example(label="")
@example(label="&")
@example(label="&&")
@example(label="&a")
@example(label="a&b")
@example(label="a&&b")
@example(label="&a&b&c")
@example(label="&&a&&b&&c")
def test_remove_mnemonic_marker(label: str):
    global stop_collecting
    if stop_collecting:
        return
    
    label_copy = copy.deepcopy(label)
    try:
        expected = remove_mnemonic_marker(label_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "&" in label or label == "":
        generated_cases.append({
            "Inputs": {"label": label},
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