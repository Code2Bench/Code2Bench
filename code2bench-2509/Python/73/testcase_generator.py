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
def filter_contained_bboxes(bboxes):
    indices_to_remove = set()
    for i in range(len(bboxes)):
        for j in range(len(bboxes)):
            if i == j:
                continue
            bbox_a = bboxes[i]
            bbox_b = bboxes[j]
            is_contained = (bbox_a['column_min'] <= bbox_b['column_min'] and
                            bbox_a['row_min'] <= bbox_b['row_min'] and
                            bbox_a['column_max'] >= bbox_b['column_max'] and
                            bbox_a['row_max'] >= bbox_b['row_max'])
            if is_contained:
                indices_to_remove.add(j)
    filtered_bboxes = [bbox for i, bbox in enumerate(bboxes) if i not in indices_to_remove]
    return filtered_bboxes

# Strategy for generating bounding boxes
def bbox_strategy():
    return st.fixed_dictionaries({
        'column_min': st.integers(min_value=0, max_value=100),
        'row_min': st.integers(min_value=0, max_value=100),
        'column_max': st.integers(min_value=0, max_value=100),
        'row_max': st.integers(min_value=0, max_value=100)
    }).filter(lambda bbox: bbox['column_min'] <= bbox['column_max'] and bbox['row_min'] <= bbox['row_max'])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(bboxes=st.lists(bbox_strategy(), min_size=1, max_size=10))
@example(bboxes=[{'column_min': 0, 'row_min': 0, 'column_max': 10, 'row_max': 10}])
@example(bboxes=[{'column_min': 0, 'row_min': 0, 'column_max': 10, 'row_max': 10},
                 {'column_min': 1, 'row_min': 1, 'column_max': 9, 'row_max': 9}])
@example(bboxes=[{'column_min': 0, 'row_min': 0, 'column_max': 10, 'row_max': 10},
                 {'column_min': 0, 'row_min': 0, 'column_max': 10, 'row_max': 10}])
@example(bboxes=[{'column_min': 0, 'row_min': 0, 'column_max': 10, 'row_max': 10},
                 {'column_min': 11, 'row_min': 11, 'column_max': 20, 'row_max': 20}])
def test_filter_contained_bboxes(bboxes):
    global stop_collecting
    if stop_collecting:
        return
    
    bboxes_copy = copy.deepcopy(bboxes)
    try:
        expected = filter_contained_bboxes(bboxes_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Ensure the test case is meaningful by checking if any bbox is contained within another
    indices_to_remove = set()
    for i in range(len(bboxes)):
        for j in range(len(bboxes)):
            if i == j:
                continue
            bbox_a = bboxes[i]
            bbox_b = bboxes[j]
            is_contained = (bbox_a['column_min'] <= bbox_b['column_min'] and
                            bbox_a['row_min'] <= bbox_b['row_min'] and
                            bbox_a['column_max'] >= bbox_b['column_max'] and
                            bbox_a['row_max'] >= bbox_b['row_max'])
            if is_contained:
                indices_to_remove.add(j)
    
    if len(indices_to_remove) > 0 or len(bboxes) == 1:
        generated_cases.append({
            "Inputs": {"bboxes": bboxes},
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