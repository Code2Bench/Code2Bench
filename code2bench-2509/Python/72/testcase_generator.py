from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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
def _generate_episode_range_string(episode_indices: List[int]) -> str:
    """
    将分集编号列表转换为紧凑的字符串表示形式。
    例如: [1, 2, 3, 5, 8, 9, 10] -> "1-3, 5, 8-10"
    """
    if not episode_indices:
        return "无"

    indices = sorted(list(set(episode_indices)))
    if not indices:
        return "无"

    ranges = []
    start = end = indices[0]

    for i in range(1, len(indices)):
        if indices[i] == end + 1:
            end = indices[i]
        else:
            ranges.append(str(start) if start == end else f"{start}-{end}")
            start = end = indices[i]
    ranges.append(str(start) if start == end else f"{start}-{end}")
    return ", ".join(ranges)

# Strategy for generating episode indices
episode_indices_strategy = st.lists(
    st.integers(min_value=0, max_value=100),  # Restrict to reasonable episode numbers
    min_size=0, max_size=20, unique=True
)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(episode_indices=episode_indices_strategy)
@example(episode_indices=[])
@example(episode_indices=[1])
@example(episode_indices=[1, 2, 3])
@example(episode_indices=[1, 3, 5])
@example(episode_indices=[1, 2, 3, 5, 8, 9, 10])
@example(episode_indices=[1, 2, 3, 5, 8, 9, 10, 12, 13, 14])
@example(episode_indices=[1, 1, 2, 2, 3])  # Duplicates
def test_generate_episode_range_string(episode_indices: List[int]):
    global stop_collecting
    if stop_collecting:
        return
    
    episode_indices_copy = copy.deepcopy(episode_indices)
    try:
        expected = _generate_episode_range_string(episode_indices_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to ensure meaningful test cases
    if len(episode_indices) > 1 or not episode_indices:
        generated_cases.append({
            "Inputs": {"episode_indices": episode_indices},
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