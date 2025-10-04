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
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

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
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(df=df_strategy(), shifts=shifts_strategy())
@example(df=pd.DataFrame(), shifts=[])
@example(df=pd.DataFrame({'A': [1, 2, 3]}), shifts=[1])
@example(df=pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}), shifts=[1, 2])
@example(df=pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}), shifts=[1, 2, 3])
def test_double_columns(df: pd.DataFrame, shifts: List[int]):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy inputs to avoid modification
    df_copy = copy.deepcopy(df)
    shifts_copy = copy.deepcopy(shifts)

    # Call func0 to verify input validity
    try:
        expected = double_columns(df_copy, shifts_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Multiple shifts with multiple columns"
        elif case_count == 1:
            desc = "Single shift with single column"
        else:
            desc = "Multiple shifts with single column"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty DataFrame and shifts"
        elif case_count == 4:
            desc = "Single shift with multiple columns"
        elif case_count == 5:
            desc = "Large number of shifts"
        elif case_count == 6:
            desc = "Single column with multiple shifts"
        else:
            desc = "Multiple columns with multiple shifts"

    # Generate usage code
    usage = f"""import pandas as pd

# Construct inputs
df = pd.DataFrame({df_copy.to_dict(orient='list')})
shifts = {shifts_copy}

# Call function
result = double_columns(df, shifts)
"""

    # Store case
    # We don't include the expected output for lib-specific types
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "df": df_copy.to_dict(orient='list'),
            "shifts": shifts_copy
        },
        "Expected": None,
        "Usage": usage
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)