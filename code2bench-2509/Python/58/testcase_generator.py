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
def insert_lines_into_block(block_bbox, line_height, page_w, page_h):
    x0, y0, x1, y1 = block_bbox

    block_height = y1 - y0
    block_weight = x1 - x0

    if line_height * 2 < block_height:
        if (
            block_height > page_h * 0.25 and page_w * 0.5 > block_weight > page_w * 0.25
        ):
            lines = int(block_height / line_height) + 1
        else:
            if block_weight > page_w * 0.4:
                lines = 3
                line_height = (y1 - y0) / lines
            elif block_weight > page_w * 0.25:
                lines = int(block_height / line_height) + 1
            else:
                if block_height / block_weight > 1.2:
                    return [[x0, y0, x1, y1]]
                else:
                    lines = 2
                    line_height = (y1 - y0) / lines

        current_y = y0

        lines_positions = []

        for i in range(lines):
            lines_positions.append([x0, current_y, x1, current_y + line_height])
            current_y += line_height
        return lines_positions

    else:
        return [[x0, y0, x1, y1]]

# Strategy for generating block_bbox
def block_bbox_strategy():
    return st.tuples(
        st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False)
    ).map(lambda x: (min(x[0], x[2]), min(x[1], x[3]), max(x[0], x[2]), max(x[1], x[3])))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    block_bbox=block_bbox_strategy(),
    line_height=st.floats(min_value=0.1, max_value=1000, allow_nan=False, allow_infinity=False),
    page_w=st.floats(min_value=1, max_value=1000, allow_nan=False, allow_infinity=False),
    page_h=st.floats(min_value=1, max_value=1000, allow_nan=False, allow_infinity=False)
)
@example(block_bbox=(0, 0, 100, 100), line_height=10, page_w=500, page_h=500)
@example(block_bbox=(0, 0, 200, 100), line_height=20, page_w=500, page_h=500)
@example(block_bbox=(0, 0, 50, 100), line_height=30, page_w=500, page_h=500)
@example(block_bbox=(0, 0, 300, 100), line_height=40, page_w=500, page_h=500)
@example(block_bbox=(0, 0, 100, 200), line_height=50, page_w=500, page_h=500)
def test_insert_lines_into_block(block_bbox, line_height, page_w, page_h):
    global stop_collecting
    if stop_collecting:
        return

    block_bbox_copy = copy.deepcopy(block_bbox)
    line_height_copy = copy.deepcopy(line_height)
    page_w_copy = copy.deepcopy(page_w)
    page_h_copy = copy.deepcopy(page_h)

    try:
        expected = insert_lines_into_block(block_bbox_copy, line_height_copy, page_w_copy, page_h_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"block_bbox": block_bbox, "line_height": line_height, "page_w": page_w, "page_h": page_h},
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