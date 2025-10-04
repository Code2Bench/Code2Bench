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
def deep_merge(defaults, current):
    """Recursively merge defaults into current, overwriting type mismatches and adding missing fields."""
    if not isinstance(defaults, dict) or not isinstance(current, dict):
        return defaults
    merged = dict(current)
    for k, v in defaults.items():
        if k not in merged:
            merged[k] = v
        else:
            if isinstance(v, dict) and isinstance(merged[k], dict):
                merged[k] = deep_merge(v, merged[k])
            elif type(merged[k]) != type(v):
                merged[k] = v
    # Optionally remove keys not in defaults (strict sync)
    # for k in list(merged.keys()):
    #     if k not in defaults:
    #         del merged[k]
    return merged

# Strategy for JSON-like objects
json_strategy = st.recursive(
    st.one_of([
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
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
@given(defaults=json_strategy, current=json_strategy)
@example(defaults={}, current={})
@example(defaults={"a": 1}, current={"a": 2})
@example(defaults={"a": {"b": 1}}, current={"a": {"c": 2}})
@example(defaults={"a": 1}, current={"a": "string"})
@example(defaults={"a": [1]}, current={"a": [2]})
@example(defaults={"a": {"b": 1}}, current={"a": 2})
def test_deep_merge(defaults, current):
    global stop_collecting
    if stop_collecting:
        return
    
    defaults_copy = copy.deepcopy(defaults)
    current_copy = copy.deepcopy(current)
    try:
        expected = deep_merge(defaults_copy, current_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(defaults, dict) or isinstance(current, dict):
        generated_cases.append({
            "Inputs": {"defaults": defaults, "current": current},
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