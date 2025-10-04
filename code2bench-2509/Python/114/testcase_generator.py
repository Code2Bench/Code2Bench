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
def CalculateAlpha(
    distances,
    fade_end=10,
    fade_start=30,
    max_fade_start=150,
    max_fade_end=170,
    verbose=False,
):
    if not distances:
        return 0

    # Calculate the average distance
    avg_distance = sum(distances) / len(distances)

    # Determine the alpha value based on the average distance
    if avg_distance < fade_end:
        return 0
    elif fade_end <= avg_distance < fade_start:
        return 255 * (avg_distance - fade_end) / (fade_start - fade_end)
    elif fade_start <= avg_distance < max_fade_start:
        return 255
    elif max_fade_start <= avg_distance < max_fade_end:
        return 255 * (max_fade_end - avg_distance) / (max_fade_end - max_fade_start)
    else:
        return 0

# Strategy for generating distances
def distances_strategy():
    return st.lists(
        st.floats(min_value=0, max_value=200, allow_nan=False, allow_infinity=False),
        min_size=1,
        max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    distances=distances_strategy(),
    fade_end=st.integers(min_value=0, max_value=30),
    fade_start=st.integers(min_value=10, max_value=50),
    max_fade_start=st.integers(min_value=100, max_value=200),
    max_fade_end=st.integers(min_value=150, max_value=250),
    verbose=st.booleans()
)
@example(distances=[], fade_end=10, fade_start=30, max_fade_start=150, max_fade_end=170, verbose=False)
@example(distances=[5], fade_end=10, fade_start=30, max_fade_start=150, max_fade_end=170, verbose=False)
@example(distances=[20], fade_end=10, fade_start=30, max_fade_start=150, max_fade_end=170, verbose=False)
@example(distances=[40], fade_end=10, fade_start=30, max_fade_start=150, max_fade_end=170, verbose=False)
@example(distances=[160], fade_end=10, fade_start=30, max_fade_start=150, max_fade_end=170, verbose=False)
@example(distances=[180], fade_end=10, fade_start=30, max_fade_start=150, max_fade_end=170, verbose=False)
def test_CalculateAlpha(distances, fade_end, fade_start, max_fade_start, max_fade_end, verbose):
    global stop_collecting
    if stop_collecting:
        return

    distances_copy = copy.deepcopy(distances)
    try:
        expected = CalculateAlpha(distances_copy, fade_end, fade_start, max_fade_start, max_fade_end, verbose)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {
            "distances": distances,
            "fade_end": fade_end,
            "fade_start": fade_start,
            "max_fade_start": max_fade_start,
            "max_fade_end": max_fade_end,
            "verbose": verbose
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