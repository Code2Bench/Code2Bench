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
def greedy_partition(seqlen_list: List[int], k_partitions: int, equal_size: bool):
    bias = sum(seqlen_list) + 1 if equal_size else 0
    sorted_seqlen = [(seqlen + bias, i) for i, seqlen in enumerate(seqlen_list)]
    partitions = [[] for _ in range(k_partitions)]
    partition_sums = [0 for _ in range(k_partitions)]
    for seqlen, i in sorted_seqlen:
        min_idx = None
        for j in range(k_partitions):
            if min_idx is None or partition_sums[j] < partition_sums[min_idx]:
                min_idx = j
        partitions[min_idx].append(i)
        partition_sums[min_idx] += seqlen
    if equal_size:
        for i, partition in enumerate(partitions):
            assert len(partition) * k_partitions == len(seqlen_list), (
                f"{len(partition)} * {k_partitions} != {len(seqlen_list)}"
            )
    return partitions

# Strategy for generating seqlen_list
def seqlen_list_strategy():
    return st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=20)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    seqlen_list=seqlen_list_strategy(),
    k_partitions=st.integers(min_value=1, max_value=20),
    equal_size=st.booleans()
)
@example(seqlen_list=[1, 2, 3], k_partitions=2, equal_size=True)
@example(seqlen_list=[1, 2, 3], k_partitions=2, equal_size=False)
@example(seqlen_list=[10, 20, 30, 40], k_partitions=3, equal_size=True)
@example(seqlen_list=[10, 20, 30, 40], k_partitions=3, equal_size=False)
@example(seqlen_list=[5, 5, 5, 5, 5], k_partitions=5, equal_size=True)
@example(seqlen_list=[5, 5, 5, 5, 5], k_partitions=5, equal_size=False)
def test_greedy_partition(seqlen_list, k_partitions, equal_size):
    global stop_collecting
    if stop_collecting:
        return
    
    if k_partitions > len(seqlen_list):
        return  # Skip invalid cases where k_partitions > len(seqlen_list)
    
    seqlen_list_copy = copy.deepcopy(seqlen_list)
    try:
        expected = greedy_partition(seqlen_list_copy, k_partitions, equal_size)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"seqlen_list": seqlen_list, "k_partitions": k_partitions, "equal_size": equal_size},
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