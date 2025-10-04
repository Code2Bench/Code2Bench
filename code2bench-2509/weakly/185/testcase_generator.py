from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
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
def nms(boxes, scores, nms_thr):
    """Single class NMS implemented in Numpy."""
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= nms_thr)[0]
        order = order[inds + 1]

    return keep

# Strategies for generating inputs
def boxes_strategy(num_boxes):
    return hnp.arrays(
        dtype=np.float32,
        shape=(num_boxes, 4),
        elements=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    )

def scores_strategy(num_boxes):
    return hnp.arrays(
        dtype=np.float32,
        shape=(num_boxes,),
        elements=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
    )

def nms_thr_strategy():
    return st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    num_boxes=st.integers(min_value=1, max_value=10),
    boxes=st.builds(lambda n: boxes_strategy(n), st.integers(min_value=1, max_value=10)),
    scores=st.builds(lambda n: scores_strategy(n), st.integers(min_value=1, max_value=10)),
    nms_thr=nms_thr_strategy()
)
@example(
    num_boxes=1,
    boxes=np.array([[0.0, 0.0, 1.0, 1.0]], dtype=np.float32),
    scores=np.array([0.5], dtype=np.float32),
    nms_thr=0.5
)
@example(
    num_boxes=2,
    boxes=np.array([[0.0, 0.0, 1.0, 1.0], [0.5, 0.5, 1.5, 1.5]], dtype=np.float32),
    scores=np.array([0.5, 0.6], dtype=np.float32),
    nms_thr=0.5
)
@example(
    num_boxes=3,
    boxes=np.array([[0.0, 0.0, 1.0, 1.0], [0.5, 0.5, 1.5, 1.5], [0.0, 0.0, 2.0, 2.0]], dtype=np.float32),
    scores=np.array([0.5, 0.6, 0.7], dtype=np.float32),
    nms_thr=0.3
)
def test_nms(num_boxes, boxes, scores, nms_thr):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    boxes_copy = copy.deepcopy(boxes)
    scores_copy = copy.deepcopy(scores)
    nms_thr_copy = copy.deepcopy(nms_thr)

    # Call func0 to verify input validity
    try:
        expected = nms(boxes_copy, scores_copy, nms_thr_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "boxes": boxes_copy.tolist(),
            "scores": scores_copy.tolist(),
            "nms_thr": nms_thr_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)