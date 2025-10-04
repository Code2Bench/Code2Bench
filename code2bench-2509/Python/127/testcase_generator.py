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
def get_predicates(conds):
    preds = []
    if isinstance(conds, str):
        return preds
    assert isinstance(conds, list)
    contains_list = any(isinstance(ele, list) for ele in conds)
    if contains_list:
        for ele in conds:
            preds += get_predicates(ele)
    else:
        preds.append(conds[0])
    return preds

# Strategy for generating nested lists and strings
def conds_strategy():
    return st.recursive(
        st.one_of([
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10), min_size=1, max_size=5)
        ]),
        lambda children: st.lists(children, min_size=1, max_size=5),
        max_leaves=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(conds=conds_strategy())
@example(conds="single_string")
@example(conds=["predicate"])
@example(conds=[["nested_predicate"]])
@example(conds=["pred1", "pred2"])
@example(conds=[["pred1", "pred2"], ["pred3"]])
@example(conds=[[["deeply_nested_predicate"]]])
def test_get_predicates(conds):
    global stop_collecting
    if stop_collecting:
        return
    
    conds_copy = copy.deepcopy(conds)
    try:
        expected = get_predicates(conds_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(conds, list) and any(isinstance(ele, list) for ele in conds):
        generated_cases.append({
            "Inputs": {"conds": conds},
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