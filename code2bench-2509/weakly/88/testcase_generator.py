from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
from datetime import datetime

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _update_head_date(data):
    """Parse data and update date of last bump in it
    :param data: String to parse for
    :returns: string with current date instead of old one
    """
    return re.sub(
        r'### HEAD as of [0-9.]{10} ###',
        "### HEAD as of {:%d.%m.%Y} ###".format(datetime.now()),
        data)

# Strategy for generating input data
def data_strategy():
    # Generate strings that may or may not contain the HEAD pattern
    return st.one_of(
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
            min_size=0,
            max_size=100
        ),
        st.builds(
            lambda s: f"### HEAD as of {s} ###",
            st.text(
                alphabet=st.characters(whitelist_categories=('N'), whitelist_characters='.'),
                min_size=10,
                max_size=10
            )
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(data=data_strategy())
@example(data="")
@example(data="### HEAD as of 01.01.2023 ###")
@example(data="random text without HEAD pattern")
@example(data="### HEAD as of 31.12.2022 ### some other text")
def test_update_head_date(data: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    data_copy = copy.deepcopy(data)

    # Call func0 to verify input validity
    try:
        expected = _update_head_date(data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "data": data_copy
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