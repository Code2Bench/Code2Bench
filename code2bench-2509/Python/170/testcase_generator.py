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
def update_yaml_dict(yaml_dict, vocabulary):
    for key, value in vocabulary.items():
        if key not in yaml_dict:
            yaml_dict[key] = value
        elif isinstance(value, dict) and isinstance(yaml_dict[key], dict):
            update_yaml_dict(yaml_dict[key], value)
    return yaml_dict

# Strategy for generating nested dictionaries
def nested_dict_strategy():
    return st.recursive(
        st.dictionaries(
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
            st.one_of([
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=5),
                st.booleans()
            ]),
            max_size=5
        ),
        lambda children: st.dictionaries(
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
            children,
            max_size=5
        ),
        max_leaves=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(yaml_dict=nested_dict_strategy(), vocabulary=nested_dict_strategy())
@example(yaml_dict={}, vocabulary={})
@example(yaml_dict={"a": 1}, vocabulary={"a": 2})
@example(yaml_dict={"a": {"b": 1}}, vocabulary={"a": {"c": 2}})
@example(yaml_dict={"a": 1}, vocabulary={"b": 2})
@example(yaml_dict={"a": {"b": 1}}, vocabulary={"a": {"b": 2}})
@example(yaml_dict={"a": {"b": 1}}, vocabulary={"a": {"b": {"c": 1}}})
def test_update_yaml_dict(yaml_dict, vocabulary):
    global stop_collecting
    if stop_collecting:
        return
    
    yaml_dict_copy = copy.deepcopy(yaml_dict)
    vocabulary_copy = copy.deepcopy(vocabulary)
    try:
        expected = update_yaml_dict(yaml_dict_copy, vocabulary_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(vocabulary, dict) and any(isinstance(value, dict) for value in vocabulary.values()):
        generated_cases.append({
            "Inputs": {"yaml_dict": yaml_dict, "vocabulary": vocabulary},
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