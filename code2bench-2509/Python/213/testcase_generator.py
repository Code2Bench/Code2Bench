from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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
def _collapse_repeated_lines(lines: List[str]) -> List[str]:
    if not lines:
        return []
    collapsed_lines = []
    prev_line = lines[0]
    count = 1
    for line in lines[1:]:
        if line == prev_line:
            count += 1
        else:
            if count > 1:
                collapsed_lines.append(f"{prev_line} (Repeated {count} times)")
            else:
                collapsed_lines.append(prev_line)
            prev_line = line
            count = 1
    if count > 1:
        collapsed_lines.append(f"{prev_line} (Repeated {count} times)")
    else:
        collapsed_lines.append(prev_line)
    return collapsed_lines

# Strategy for generating lines of text
def line_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(lines=st.lists(line_strategy(), min_size=0, max_size=20))
@example(lines=[])
@example(lines=["single_line"])
@example(lines=["line1", "line1"])
@example(lines=["line1", "line1", "line2"])
@example(lines=["line1", "line1", "line2", "line2", "line2"])
@example(lines=["line1", "line2", "line3"])
def test_collapse_repeated_lines(lines: List[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    lines_copy = copy.deepcopy(lines)
    try:
        expected = _collapse_repeated_lines(lines_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to prioritize cases with repeated lines or empty lists
    if not lines or any(lines.count(line) > 1 for line in lines):
        generated_cases.append({
            "Inputs": {"lines": lines},
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