from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Dict, Optional, Tuple

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def get_contest_data_from_cache(contest_id: int, cached_data: Dict) -> Tuple[Optional[Dict], Optional[Dict]]:
    contest_id_str = str(contest_id)

    if contest_id_str not in cached_data:
        print(f"Warning: Contest {contest_id} data not found in cache")
        return None, None

    contest_data = cached_data[contest_id_str]

    try:
        standings = contest_data["standings"]
        rating_changes = contest_data["rating_changes"]

        if standings.get("status") != "OK" or rating_changes.get("status") != "OK":
            print(f"Warning: Contest {contest_id} cached data status abnormal")
            return None, None

        return standings, rating_changes

    except KeyError as e:
        print(f"Warning: Contest {contest_id} cached data structure abnormal: {e}")
        return None, None

# Strategies for generating inputs
def contest_id_strategy():
    return st.integers(min_value=0, max_value=1000)

def cached_data_strategy():
    return st.dictionaries(
        keys=st.text(min_size=1, max_size=10),
        values=st.dictionaries(
            keys=st.sampled_from(["standings", "rating_changes"]),
            values=st.dictionaries(
                keys=st.text(min_size=1, max_size=20),
                values=st.text(min_size=1, max_size=20) | st.integers() | st.floats(),
                min_size=1,
                max_size=5
            ),
            min_size=2,
            max_size=2
        ),
        min_size=0,
        max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    contest_id=contest_id_strategy(),
    cached_data=cached_data_strategy()
)
@example(
    contest_id=1,
    cached_data={}
)
@example(
    contest_id=2,
    cached_data={"2": {"standings": {"status": "OK"}, "rating_changes": {"status": "OK"}}}
)
@example(
    contest_id=3,
    cached_data={"3": {"standings": {"status": "FAIL"}, "rating_changes": {"status": "OK"}}}
)
@example(
    contest_id=4,
    cached_data={"4": {"standings": {"status": "OK"}, "rating_changes": {"status": "FAIL"}}}
)
@example(
    contest_id=5,
    cached_data={"5": {"standings": {"status": "FAIL"}, "rating_changes": {"status": "FAIL"}}}
)
@example(
    contest_id=6,
    cached_data={"6": {"standings": {}, "rating_changes": {}}}
)
def test_get_contest_data_from_cache(contest_id: int, cached_data: Dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    contest_id_copy = contest_id
    cached_data_copy = copy.deepcopy(cached_data)

    # Call func0 to verify input validity
    try:
        standings, rating_changes = get_contest_data_from_cache(contest_id_copy, cached_data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "contest_id": contest_id_copy,
            "cached_data": cached_data_copy
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