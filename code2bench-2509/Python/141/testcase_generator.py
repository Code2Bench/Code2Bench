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
def count_todos(obj) -> int:
    """Count TODO: translate entries in a dict or list."""
    if isinstance(obj, dict):
        return sum(count_todos(v) for v in obj.values())
    if isinstance(obj, list):
        return sum(count_todos(v) for v in obj)
    if isinstance(obj, str) and obj.strip().startswith("TODO: translate"):
        return 1
    return 0

# Strategy for generating JSON-like objects with TODO strings
def todo_strategy():
    return st.one_of([
        st.just("TODO: translate"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))).filter(lambda x: not x.strip().startswith("TODO: translate"))
    ])

json_strategy = st.recursive(
    st.one_of([
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        todo_strategy(),
        st.booleans()
    ]),
    lambda children: st.one_of(
        st.lists(children, max_size=5),
        st.dictionaries(st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5), children, max_size=5)
    ),
    max_leaves=5
)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(obj=json_strategy)
@example(obj={})
@example(obj=[])
@example(obj="TODO: translate")
@example(obj="Not a TODO")
@example(obj={"key": "TODO: translate"})
@example(obj=["TODO: translate", "Not a TODO"])
@example(obj={"nested": {"key": "TODO: translate"}})
@example(obj=[{"key": "TODO: translate"}, "Not a TODO"])
def test_count_todos(obj):
    global stop_collecting
    if stop_collecting:
        return
    
    obj_copy = copy.deepcopy(obj)
    try:
        expected = count_todos(obj_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(obj, (dict, list)) or (isinstance(obj, str) and obj.strip().startswith("TODO: translate")):
        generated_cases.append({
            "Inputs": {"obj": obj},
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