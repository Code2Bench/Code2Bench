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
def validate_input_media(width, height, with_frame_conditioning, num_frames_in=None):
    if num_frames_in and not num_frames_in % 16 == 0:
        return False, ("The input video total frame count must be divisible by 16!")

    if height % 8 != 0 or width % 8 != 0:
        return False, (
            f"Height ({height}) and width ({width}) must be " "divisible by 8"
        )

    if with_frame_conditioning:
        if (height * width) % 8192 != 0:
            return False, (
                f"Height * width ({height * width}) must be "
                "divisible by 8192 for frame conditioning"
            )
    else:
        if num_frames_in and not num_frames_in % 32 == 0:
            return False, ("The input video total frame count must be divisible by 32!")
    return True, "Validation successful"

# Strategy for generating inputs
def width_strategy():
    return st.integers(min_value=8, max_value=4096).filter(lambda x: x % 8 == 0)

def height_strategy():
    return st.integers(min_value=8, max_value=4096).filter(lambda x: x % 8 == 0)

def num_frames_strategy():
    return st.one_of([
        st.none(),
        st.integers(min_value=16, max_value=1024).filter(lambda x: x % 16 == 0),
        st.integers(min_value=16, max_value=1024).filter(lambda x: x % 32 == 0)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    width=width_strategy(),
    height=height_strategy(),
    with_frame_conditioning=st.booleans(),
    num_frames_in=num_frames_strategy()
)
@example(width=16, height=16, with_frame_conditioning=True, num_frames_in=16)
@example(width=16, height=16, with_frame_conditioning=False, num_frames_in=32)
@example(width=16, height=16, with_frame_conditioning=True, num_frames_in=None)
@example(width=16, height=16, with_frame_conditioning=False, num_frames_in=None)
@example(width=8, height=8, with_frame_conditioning=True, num_frames_in=16)
@example(width=8, height=8, with_frame_conditioning=False, num_frames_in=32)
def test_validate_input_media(width, height, with_frame_conditioning, num_frames_in):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = validate_input_media(width, height, with_frame_conditioning, num_frames_in)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {
            "width": width,
            "height": height,
            "with_frame_conditioning": with_frame_conditioning,
            "num_frames_in": num_frames_in
        },
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