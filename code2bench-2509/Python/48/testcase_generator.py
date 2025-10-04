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
def separate_lora_AB(parameters, B_patterns=None):
    parameters_normal = {}
    parameters_B = {}

    if B_patterns is None:
        B_patterns = ['.lora_B.', '__zero__']

    for k, v in parameters.items():
        if any(B_pattern in k for B_pattern in B_patterns):
            parameters_B[k] = v
        else:
            parameters_normal[k] = v

    return parameters_normal, parameters_B

# Strategy for generating parameter keys
def key_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20).map(lambda x: f"{x}.lora_B.{x}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20).map(lambda x: f"{x}__zero__{x}")
    ])

# Strategy for generating parameters dictionary
def parameters_strategy():
    return st.dictionaries(
        keys=key_strategy(),
        values=st.floats(allow_nan=False, allow_infinity=False, width=32),
        min_size=1,
        max_size=10
    )

# Strategy for generating B_patterns
def B_patterns_strategy():
    return st.one_of([
        st.just(None),
        st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10), min_size=1, max_size=5)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(parameters=parameters_strategy(), B_patterns=B_patterns_strategy())
@example(parameters={"key.lora_B.key": 1.0}, B_patterns=None)
@example(parameters={"key__zero__key": 1.0}, B_patterns=None)
@example(parameters={"key": 1.0}, B_patterns=None)
@example(parameters={"key.lora_B.key": 1.0, "key": 2.0}, B_patterns=None)
@example(parameters={"key.lora_B.key": 1.0}, B_patterns=[".lora_B."])
@example(parameters={"key__zero__key": 1.0}, B_patterns=["__zero__"])
@example(parameters={"key": 1.0}, B_patterns=[".lora_B.", "__zero__"])
def test_separate_lora_AB(parameters, B_patterns):
    global stop_collecting
    if stop_collecting:
        return
    
    parameters_copy = copy.deepcopy(parameters)
    B_patterns_copy = copy.deepcopy(B_patterns)
    try:
        expected = separate_lora_AB(parameters_copy, B_patterns_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(".lora_B." in k or "__zero__" in k for k in parameters) or B_patterns is not None:
        generated_cases.append({
            "Inputs": {"parameters": parameters, "B_patterns": B_patterns},
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