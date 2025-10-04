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
def split_parameters(params_str: str) -> list:
    """Split parameter string by commas, handling nested types."""
    params = []
    current_param = ""
    depth = 0

    for char in params_str:
        if char in "<[{(":
            depth += 1
        elif char in ">]})":
            depth -= 1
        elif char == "," and depth == 0:
            params.append(current_param)
            current_param = ""
            continue

        current_param += char

    if current_param:
        params.append(current_param)

    return params

# Strategy for generating parameter strings
def param_strategy():
    return st.one_of([
        # Simple parameters
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
        # Nested parameters
        st.recursive(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=5),
            lambda children: st.one_of([
                st.tuples(st.just("<"), children, st.just(">")),
                st.tuples(st.just("["), children, st.just("]")),
                st.tuples(st.just("{"), children, st.just("}")),
                st.tuples(st.just("("), children, st.just(")")),
            ]).map(lambda x: "".join(x)),
            max_leaves=5
        ),
        # Multiple parameters with nested types
        st.lists(
            st.one_of([
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=5),
                st.recursive(
                    st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=5),
                    lambda children: st.one_of([
                        st.tuples(st.just("<"), children, st.just(">")),
                        st.tuples(st.just("["), children, st.just("]")),
                        st.tuples(st.just("{"), children, st.just("}")),
                        st.tuples(st.just("("), children, st.just(")")),
                    ]).map(lambda x: "".join(x)),
                    max_leaves=5
                )
            ]),
            min_size=1, max_size=5
        ).map(lambda x: ",".join(x))
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(params_str=param_strategy())
@example(params_str="a,b,c")
@example(params_str="a<b,c>")
@example(params_str="a[b,c],d")
@example(params_str="a{b,c},d")
@example(params_str="a(b,c),d")
@example(params_str="a<b<c>>,d")
@example(params_str="a[b[c]],d")
@example(params_str="a{b{c}},d")
@example(params_str="a(b(c)),d")
@example(params_str="")
def test_split_parameters(params_str: str):
    global stop_collecting
    if stop_collecting:
        return
    
    params_str_copy = copy.deepcopy(params_str)
    try:
        expected = split_parameters(params_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(char in "<[{(" for char in params_str) or "," in params_str:
        generated_cases.append({
            "Inputs": {"params_str": params_str},
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