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
def valid_cluster_shape(cc: int, cluster_shape: list) -> tuple:
    if cc < 90:
        if cluster_shape != [1, 1, 1]:
            return (False,
                    f"Cluster shape for pre-SM90 architectures must be [1, 1, 1]. Received cluster shape of "
                    f"{cluster_shape} for SM{cc}.")
        else:
            return (True, "")

    if len(cluster_shape) != 3:
        return (False,
                f"Cluster shapes must be rank-3. Received {cluster_shape} (rank {len(cluster_shape)}")

    if cluster_shape[2] != 1:
        return (False,
                "CUTLASS kernels currently require the third dimension of cluster shape to be 1. "
                f"Received cluster shape of {cluster_shape}.")

    blocks_in_2d = cluster_shape[0] * cluster_shape[1]
    if blocks_in_2d > 8:
        return (False,
            f"Thread block clusters with more than 8 thread blocks are currently unsupported on SM{cc}. "
            f"Received cluster shape {cluster_shape}, which has {blocks_in_2d} thread blocks.")
    return (True, "")

# Strategy for generating compute capability (cc)
cc_strategy = st.integers(min_value=50, max_value=120)

# Strategy for generating cluster shapes
def cluster_shape_strategy():
    return st.lists(st.integers(min_value=1, max_value=10), min_size=3, max_size=3)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(cc=cc_strategy, cluster_shape=cluster_shape_strategy())
@example(cc=89, cluster_shape=[1, 1, 1])
@example(cc=89, cluster_shape=[2, 2, 2])
@example(cc=90, cluster_shape=[1, 1, 1])
@example(cc=90, cluster_shape=[2, 2, 1])
@example(cc=90, cluster_shape=[3, 3, 1])
@example(cc=90, cluster_shape=[4, 2, 1])
@example(cc=90, cluster_shape=[2, 2, 2])
@example(cc=90, cluster_shape=[1, 1, 2])
@example(cc=90, cluster_shape=[1, 1, 0])
@example(cc=90, cluster_shape=[1, 1])
def test_valid_cluster_shape(cc, cluster_shape):
    global stop_collecting
    if stop_collecting:
        return
    
    cluster_shape_copy = copy.deepcopy(cluster_shape)
    try:
        expected = valid_cluster_shape(cc, cluster_shape_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"cc": cc, "cluster_shape": cluster_shape},
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