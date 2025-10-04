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
def conditioning_set_values(conditioning, values={}, append=False):
    c = []
    for t in conditioning:
        n = [t[0], t[1].copy()]
        for k in values:
            val = values[k]
            if append:
                old_val = n[1].get(k, None)
                if old_val is not None:
                    val = old_val + val

            n[1][k] = val
        c.append(n)

    return c

# Strategy for generating conditioning
def conditioning_strategy():
    return st.lists(
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.dictionaries(
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
                st.one_of([
                    st.integers(),
                    st.floats(allow_nan=False, allow_infinity=False),
                    st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
                ]),
                max_size=5
            )
        ),
        min_size=1, max_size=5
    )

# Strategy for generating values
def values_strategy():
    return st.dictionaries(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        st.one_of([
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ]),
        max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    conditioning=conditioning_strategy(),
    values=values_strategy(),
    append=st.booleans()
)
@example(conditioning=[("key1", {"a": 1})], values={"a": 2}, append=False)
@example(conditioning=[("key1", {"a": 1})], values={"a": 2}, append=True)
@example(conditioning=[("key1", {"a": "hello"})], values={"a": "world"}, append=True)
@example(conditioning=[("key1", {"a": 1.5})], values={"a": 2.5}, append=False)
@example(conditioning=[("key1", {"a": 1}), ("key2", {"b": 2})], values={"a": 3, "b": 4}, append=True)
def test_conditioning_set_values(conditioning, values, append):
    global stop_collecting
    if stop_collecting:
        return
    
    conditioning_copy = copy.deepcopy(conditioning)
    values_copy = copy.deepcopy(values)
    try:
        expected = conditioning_set_values(conditioning_copy, values_copy, append)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"conditioning": conditioning, "values": values, "append": append},
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