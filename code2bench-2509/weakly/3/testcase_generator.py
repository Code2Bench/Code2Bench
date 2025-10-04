from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import math
import json
import os
import atexit
import copy
from typing import Tuple

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def make_shifted_720Pwindows_bysize(size: Tuple[int, int, int], num_windows: Tuple[int, int, int]):
    t, h, w = size
    resized_nt, resized_nh, resized_nw = num_windows
    #cal windows under 720p
    scale = math.sqrt((45 * 80) / (h * w))
    resized_h, resized_w = round(h * scale), round(w * scale)
    wh, ww = math.ceil(resized_h / resized_nh), math.ceil(resized_w / resized_nw)  # window size.
    wt = math.ceil(min(t, 30) / resized_nt)  # window size.

    st, sh, sw = (  # shift size.
        0.5 if wt < t else 0,
        0.5 if wh < h else 0,
        0.5 if ww < w else 0,
    )
    nt, nh, nw = math.ceil((t - st) / wt), math.ceil((h - sh) / wh), math.ceil((w - sw) / ww)  # window size.
    nt, nh, nw = (  # number of window.
        nt + 1 if st > 0 else 1,
        nh + 1 if sh > 0 else 1,
        nw + 1 if sw > 0 else 1,
    )
    return [
        (
            slice(max(int((it - st) * wt), 0), min(int((it - st + 1) * wt), t)),
            slice(max(int((ih - sh) * wh), 0), min(int((ih - sh + 1) * wh), h)),
            slice(max(int((iw - sw) * ww), 0), min(int((iw - sw + 1) * ww), w)),
        )
        for iw in range(nw)
        if min(int((iw - sw + 1) * ww), w) > max(int((iw - sw) * ww), 0)
        for ih in range(nh)
        if min(int((ih - sh + 1) * wh), h) > max(int((ih - sh) * wh), 0)
        for it in range(nt)
        if min(int((it - st + 1) * wt), t) > max(int((it - st) * wt), 0)
    ]

# Strategies for generating inputs
def size_strategy():
    return st.tuples(
        st.integers(min_value=1, max_value=100),  # t
        st.integers(min_value=1, max_value=100),  # h
        st.integers(min_value=1, max_value=100)   # w
    )

def num_windows_strategy():
    return st.tuples(
        st.integers(min_value=1, max_value=10),  # resized_nt
        st.integers(min_value=1, max_value=10),  # resized_nh
        st.integers(min_value=1, max_value=10)   # resized_nw
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    size=size_strategy(),
    num_windows=num_windows_strategy()
)
@example(
    size=(1, 1, 1),
    num_windows=(1, 1, 1)
)
@example(
    size=(30, 45, 80),
    num_windows=(3, 3, 3)
)
@example(
    size=(100, 100, 100),
    num_windows=(10, 10, 10)
)
def test_make_shifted_720Pwindows_bysize(size: Tuple[int, int, int], num_windows: Tuple[int, int, int]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    size_copy = copy.deepcopy(size)
    num_windows_copy = copy.deepcopy(num_windows)

    # Call func0 to verify input validity
    try:
        expected = make_shifted_720Pwindows_bysize(size_copy, num_windows_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "size": size_copy,
            "num_windows": num_windows_copy
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