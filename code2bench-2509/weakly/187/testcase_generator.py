from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import pandas as pd
import numpy as np
import json
import os
import atexit
import copy
from typing import List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def double_columns(df, shifts: List[int]):
    """
    Use previous rows as features appended to this row. This allows us to move history to the current time.
    One limitation is that this function will duplicate *all* features and only using the explicitly specified list of offsets.
    """
    if not shifts:
        return df
    df_list = [df.shift(shift) for shift in shifts]
    df_list.insert(0, df)
    max_shift = max(shifts)

    # Shift and add same columns
    df_out = pd.concat(df_list, axis=1)  # keys=('A', 'B')

    return df_out

# Strategies for generating inputs
def df_strategy():
    return st.builds(
        pd.DataFrame,
        data=hnp.arrays(
            dtype=np.float64,
            shape=st.tuples(
                st.integers(min_value=1, max_value=10),  # rows
                st.integers(min_value=1, max_value=5)   # columns
            ),
            elements=st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False)
        )
    )

def shifts_strategy():
    return st.lists(
        st.integers(min_value=1, max_value=5),
        min_size=0, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(df=df_strategy(), shifts=shifts_strategy())
@example(df=pd.DataFrame(), shifts=[])
@example(df=pd.DataFrame({'A': [1, 2, 3]}), shifts=[1])
@example(df=pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}), shifts=[1, 2])
@example(df=pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}), shifts=[1, 2, 3])
def test_double_columns(df: pd.DataFrame, shifts: List[int]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    df_copy = copy.deepcopy(df)
    shifts_copy = copy.deepcopy(shifts)

    # Call func0 to verify input validity
    try:
        expected = double_columns(df_copy, shifts_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "df": df_copy.to_dict(orient='list'),
            "shifts": shifts_copy
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