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
def _format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)

    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1

    if i == 0:
        return f"{int(size)} {size_names[i]}"
    else:
        return f"{size:.1f} {size_names[i]}"

# Strategy for generating file sizes
size_bytes_strategy = st.one_of([
    st.just(0),  # Edge case: zero bytes
    st.integers(min_value=1, max_value=1023),  # Bytes
    st.integers(min_value=1024, max_value=1024**2 - 1),  # Kilobytes
    st.integers(min_value=1024**2, max_value=1024**3 - 1),  # Megabytes
    st.integers(min_value=1024**3, max_value=1024**4 - 1),  # Gigabytes
    st.integers(min_value=1024**4, max_value=1024**5 - 1),  # Terabytes
    st.integers(min_value=1024**5, max_value=1024**6 - 1),  # Beyond terabytes
])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(size_bytes=size_bytes_strategy)
@example(size_bytes=0)
@example(size_bytes=1)
@example(size_bytes=1023)
@example(size_bytes=1024)
@example(size_bytes=1024**2)
@example(size_bytes=1024**3)
@example(size_bytes=1024**4)
@example(size_bytes=1024**5)
def test_format_file_size(size_bytes: int):
    global stop_collecting
    if stop_collecting:
        return

    size_bytes_copy = copy.deepcopy(size_bytes)
    try:
        expected = _format_file_size(size_bytes_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"size_bytes": size_bytes},
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