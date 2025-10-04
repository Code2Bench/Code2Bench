from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import itertools
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
def get_one_prot_diff_name_pairs(names):
    """
    Get all pairs of names that have a charge difference of 1.

    Assumes that the names are in the format "name_charge_spin"
    """
    name_pairs = []
    for name0, name1 in itertools.combinations(names, 2):
        name0_charge = int(name0.split("_")[-2])
        name1_charge = int(name1.split("_")[-2])
        if abs(name0_charge - name1_charge) == 1:
            name_pairs.append((name0, name1))
    return name_pairs

# Strategy for generating names in the format "name_charge_spin"
def name_strategy():
    return st.builds(
        lambda name, charge, spin: f"{name}_{charge}_{spin}",
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
        st.integers(min_value=-10, max_value=10),
        st.sampled_from(["up", "down"])
    )

# Strategy for generating lists of names
def names_strategy():
    return st.lists(name_strategy(), min_size=2, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(names=names_strategy())
@example(names=[])
@example(names=["name1_0_up", "name2_1_down"])
@example(names=["name1_0_up", "name2_1_down", "name3_2_up"])
@example(names=["name1_0_up", "name2_1_down", "name3_0_up"])
@example(names=["name1_0_up", "name2_1_down", "name3_1_up", "name4_2_down"])
def test_get_one_prot_diff_name_pairs(names):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    names_copy = copy.deepcopy(names)

    # Call func0 to verify input validity
    try:
        expected = get_one_prot_diff_name_pairs(names_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "names": names_copy
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