from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def format_duration(duration_seconds: float) -> str:
    """
    Convert seconds to a human-friendly time string

    Args:
        duration_seconds: Duration (seconds)

    Returns:
        Formatted time string, such as: 1h23m45s, 2m30s, 1.5s, 500ms
    """
    if duration_seconds < 0:
        return "0ms"

    # Convert to milliseconds
    total_ms = int(duration_seconds * 1000)

    # If less than 1 second, display milliseconds
    if total_ms < 1000:
        return f"{total_ms}ms"

    # Convert to each time unit
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    seconds = duration_seconds % 60

    # Build the time string
    time_parts = []

    if hours > 0:
        time_parts.append(f"{hours}h")

    if minutes > 0:
        time_parts.append(f"{minutes}m")

    # For seconds, if there is a decimal part and the total duration is less than 10 seconds, keep 1 decimal place
    if seconds > 0:
        if duration_seconds < 10 and seconds != int(seconds):
            time_parts.append(f"{seconds:.1f}s")
        else:
            time_parts.append(f"{int(seconds)}s")

    # If there are no time parts (theoretically should not happen), return 0ms
    if not time_parts:
        return "0ms"

    return "".join(time_parts)

# Strategy for generating duration_seconds
duration_strategy = st.one_of([
    st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=10, allow_nan=False, allow_infinity=False),
    st.floats(min_value=10, max_value=3600, allow_nan=False, allow_infinity=False),
    st.floats(min_value=3600, max_value=86400, allow_nan=False, allow_infinity=False)
])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(duration_seconds=duration_strategy)
@example(duration_seconds=0)
@example(duration_seconds=0.5)
@example(duration_seconds=1)
@example(duration_seconds=1.5)
@example(duration_seconds=60)
@example(duration_seconds=61)
@example(duration_seconds=3600)
@example(duration_seconds=3661)
@example(duration_seconds=-1)
def test_format_duration(duration_seconds: float):
    global stop_collecting
    if stop_collecting:
        return

    try:
        expected = format_duration(duration_seconds)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"duration_seconds": duration_seconds},
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