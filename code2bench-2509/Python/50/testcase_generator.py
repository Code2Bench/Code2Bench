from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict, List
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
def default_get_group_data_meta_info(temp_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    if not temp_data:
        return {
            "total_samples": 0,
            "num_groups": 0,
            "avg_group_size": 0,
            "avg_reward": 0,
        }

    meta_info = {"total_samples": 0, "num_groups": len(temp_data)}

    all_rewards = []
    # Calculate per-group statistics
    for instance_id, samples in temp_data.items():
        group_size = len(samples)
        group_rewards = [s["reward"] for s in samples]  # Calculate group reward standard deviation
        meta_info["total_samples"] += group_size
        all_rewards.extend(group_rewards)
    # Calculate global statistics
    meta_info["avg_group_size"] = meta_info["total_samples"] / meta_info["num_groups"]

    if all_rewards:
        meta_info["avg_reward"] = sum(all_rewards) / len(all_rewards)
    else:
        meta_info["avg_reward"] = 0
    return meta_info

# Strategy for generating sample dictionaries
def sample_strategy():
    return st.fixed_dictionaries({
        "reward": st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000)
    })

# Strategy for generating temp_data
def temp_data_strategy():
    return st.dictionaries(
        st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
        st.lists(sample_strategy(), min_size=0, max_size=10),
        min_size=0,
        max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(temp_data=temp_data_strategy())
@example(temp_data={})
@example(temp_data={"group1": [{"reward": 1.0}]})
@example(temp_data={"group1": [{"reward": 1.0}], "group2": [{"reward": 2.0}]})
@example(temp_data={"group1": [{"reward": 1.0}, {"reward": 2.0}]})
@example(temp_data={"group1": [], "group2": [{"reward": 3.0}]})
def test_default_get_group_data_meta_info(temp_data: Dict[str, List[Dict[str, Any]]]):
    global stop_collecting
    if stop_collecting:
        return
    
    temp_data_copy = copy.deepcopy(temp_data)
    try:
        expected = default_get_group_data_meta_info(temp_data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"temp_data": temp_data},
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