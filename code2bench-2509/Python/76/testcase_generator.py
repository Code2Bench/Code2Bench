from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List, Tuple
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
def find_context_core(
    lines: List[str], context: List[str], start: int
) -> Tuple[int, int]:
    if not context:
        return start, 0

    for i in range(start, len(lines)):
        if lines[i : i + len(context)] == context:
            return i, 0
    for i in range(start, len(lines)):
        if [s.rstrip() for s in lines[i : i + len(context)]] == [
            s.rstrip() for s in context
        ]:
            return i, 1
    for i in range(start, len(lines)):
        if [s.strip() for s in lines[i : i + len(context)]] == [
            s.strip() for s in context
        ]:
            return i, 100
    return -1, 0

# Strategy for generating lines of text
def line_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    lines=st.lists(line_strategy(), min_size=0, max_size=20),
    context=st.lists(line_strategy(), min_size=0, max_size=5),
    start=st.integers(min_value=0)
)
@example(lines=[], context=[], start=0)
@example(lines=["line1", "line2"], context=["line1"], start=0)
@example(lines=["line1 ", "line2"], context=["line1"], start=0)
@example(lines=[" line1 ", "line2"], context=["line1"], start=0)
@example(lines=["line1", "line2"], context=["line3"], start=0)
@example(lines=["line1", "line2"], context=["line1", "line2"], start=0)
@example(lines=["line1 ", "line2 "], context=["line1", "line2"], start=0)
@example(lines=[" line1 ", " line2 "], context=["line1", "line2"], start=0)
def test_find_context_core(lines: List[str], context: List[str], start: int):
    global stop_collecting
    if stop_collecting:
        return
    
    lines_copy = copy.deepcopy(lines)
    context_copy = copy.deepcopy(context)
    try:
        expected = find_context_core(lines_copy, context_copy, start)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter cases to ensure meaningful coverage
    if (len(context) > 0 and len(lines) >= len(context)) or (len(context) == 0 and start < len(lines)):
        generated_cases.append({
            "Inputs": {"lines": lines, "context": context, "start": start},
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