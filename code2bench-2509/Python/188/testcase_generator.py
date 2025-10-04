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
def compress_token_type_ids(token_type_ids: list[int]) -> int:
    """
    Return position of the first 1 or the length of the list
    if not found.
    """
    first_one = len(token_type_ids)
    err_msg = "Token type ids are expected to be a sequence"\
              " of zeros followed by a sequence of ones"
    for i, type_id in enumerate(token_type_ids):
        if type_id == 0 and first_one < i:
            raise ValueError(err_msg)
        elif type_id == 1 and first_one > i:
            first_one = i
        elif type_id > 1:
            raise ValueError(err_msg)

    return first_one

# Strategy for generating token_type_ids
def token_type_ids_strategy():
    return st.lists(
        st.one_of([st.just(0), st.just(1)]),
        min_size=0,
        max_size=20
    ).map(lambda ids: ids + [1] * (len(ids) == 0 or ids[-1] == 0))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(token_type_ids=token_type_ids_strategy())
@example(token_type_ids=[])
@example(token_type_ids=[0])
@example(token_type_ids=[1])
@example(token_type_ids=[0, 1])
@example(token_type_ids=[0, 0, 1])
@example(token_type_ids=[1, 1, 1])
@example(token_type_ids=[0, 0, 0])
def test_compress_token_type_ids(token_type_ids):
    global stop_collecting
    if stop_collecting:
        return
    
    token_type_ids_copy = copy.deepcopy(token_type_ids)
    try:
        expected = compress_token_type_ids(token_type_ids_copy)
    except ValueError:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"token_type_ids": token_type_ids},
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