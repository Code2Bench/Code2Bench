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
def functionParams(args, vars):
    params = {}
    index = 1
    for var in vars:
        value = args.get(var)
        if value is None:
            value = args.get(str(index))  # positional argument
            if value is None:
                value = ''
            else:
                index += 1
        params[var] = value
    return params

# Strategy for generating args dictionary
def args_strategy():
    return st.dictionaries(
        keys=st.one_of(
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
            st.integers(min_value=1, max_value=10).map(str)
        ),
        values=st.one_of(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.booleans()
        ),
        max_size=10
    )

# Strategy for generating vars list
def vars_strategy():
    return st.lists(
        st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
        min_size=1, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(args=args_strategy(), vars=vars_strategy())
@example(args={}, vars=["var1"])
@example(args={"var1": "value1"}, vars=["var1"])
@example(args={"1": "value1"}, vars=["var1"])
@example(args={"var1": "value1", "2": "value2"}, vars=["var1", "var2"])
@example(args={"1": "value1", "2": "value2"}, vars=["var1", "var2"])
@example(args={"var1": "value1", "var2": "value2"}, vars=["var1", "var2"])
@example(args={"1": "value1", "var2": "value2"}, vars=["var1", "var2"])
def test_functionParams(args, vars):
    global stop_collecting
    if stop_collecting:
        return
    
    args_copy = copy.deepcopy(args)
    vars_copy = copy.deepcopy(vars)
    try:
        expected = functionParams(args_copy, vars_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"args": args, "vars": vars},
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