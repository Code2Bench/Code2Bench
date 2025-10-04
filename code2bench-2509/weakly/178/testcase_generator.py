from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Iterable, Optional, Type
from collections import abc

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def iter_cast(inputs: Iterable, dst_type: Type, return_type: Optional[Type] = None):
    if not isinstance(inputs, abc.Iterable):
        raise TypeError('inputs must be an iterable object')
    if not isinstance(dst_type, type):
        raise TypeError('"dst_type" must be a valid type')

    out_iterable = map(dst_type, inputs)

    if return_type is None:
        return out_iterable
    else:
        return return_type(out_iterable)

# Strategies for generating inputs
def inputs_strategy():
    return st.one_of(
        st.lists(st.integers()),
        st.lists(st.floats()),
        st.lists(st.text()),
        st.tuples(st.integers()),
        st.tuples(st.floats()),
        st.tuples(st.text())
    )

def dst_type_strategy():
    return st.one_of(
        st.just(int),
        st.just(float),
        st.just(str)
    )

def return_type_strategy():
    return st.one_of(
        st.none(),
        st.just(list),
        st.just(tuple)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    inputs=inputs_strategy(),
    dst_type=dst_type_strategy(),
    return_type=return_type_strategy()
)
@example(inputs=[1, 2, 3], dst_type=int, return_type=list)
@example(inputs=[1.0, 2.0, 3.0], dst_type=float, return_type=tuple)
@example(inputs=["a", "b", "c"], dst_type=str, return_type=None)
@example(inputs=[], dst_type=int, return_type=list)
@example(inputs=(1, 2, 3), dst_type=int, return_type=tuple)
def test_iter_cast(inputs: Iterable, dst_type: Type, return_type: Optional[Type]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    inputs_copy = copy.deepcopy(inputs)
    dst_type_copy = copy.deepcopy(dst_type)
    return_type_copy = copy.deepcopy(return_type)

    # Call func0 to verify input validity
    try:
        result = iter_cast(inputs_copy, dst_type_copy, return_type_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "inputs": list(inputs_copy) if isinstance(inputs_copy, abc.Iterable) else inputs_copy,
            "dst_type": dst_type_copy.__name__,
            "return_type": return_type_copy.__name__ if return_type_copy is not None else None
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