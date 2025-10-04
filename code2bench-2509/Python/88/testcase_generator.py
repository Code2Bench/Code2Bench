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
def merge_overlapping_spans(spans):
    if not spans:
        return []

    spans.sort(key=lambda x: x[0])

    merged = []
    for span in spans:
        x1, y1, x2, y2 = span
        if not merged or merged[-1][2] < x1:
            merged.append(span)
        else:
            last_span = merged.pop()
            x1 = min(last_span[0], x1)
            y1 = min(last_span[1], y1)
            x2 = max(last_span[2], x2)
            y2 = max(last_span[3], y2)
            merged.append((x1, y1, x2, y2))

    return merged

# Strategy for generating span coordinates
def span_strategy():
    return st.tuples(
        st.integers(min_value=0, max_value=100),
        st.integers(min_value=0, max_value=100),
        st.integers(min_value=0, max_value=100),
        st.integers(min_value=0, max_value=100)
    ).filter(lambda x: x[0] <= x[2] and x[1] <= x[3])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(spans=st.lists(span_strategy(), min_size=0, max_size=10))
@example(spans=[])
@example(spans=[(0, 0, 10, 10)])
@example(spans=[(0, 0, 10, 10), (5, 5, 15, 15)])
@example(spans=[(0, 0, 10, 10), (20, 20, 30, 30)])
@example(spans=[(0, 0, 10, 10), (10, 10, 20, 20)])
@example(spans=[(0, 0, 10, 10), (5, 5, 15, 15), (20, 20, 30, 30)])
def test_merge_overlapping_spans(spans):
    global stop_collecting
    if stop_collecting:
        return
    
    spans_copy = copy.deepcopy(spans)
    try:
        expected = merge_overlapping_spans(spans_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if spans or any(
        span1[2] >= span2[0] and span1[3] >= span2[1]
        for i, span1 in enumerate(spans)
        for j, span2 in enumerate(spans)
        if i != j
    ):
        generated_cases.append({
            "Inputs": {"spans": spans},
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