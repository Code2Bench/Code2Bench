from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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
def _filter_invalid_triples(triples: List[List[str]]) -> List[List[str]]:
    """过滤无效的三元组"""
    unique_triples = set()
    valid_triples = []

    for triple in triples:
        if len(triple) != 3 or (
            (not isinstance(triple[0], str) or triple[0].strip() == "")
            or (not isinstance(triple[1], str) or triple[1].strip() == "")
            or (not isinstance(triple[2], str) or triple[2].strip() == "")
        ):
            # 三元组长度不为3，或其中存在空值
            continue

        valid_triple = [str(item) for item in triple]
        if tuple(valid_triple) not in unique_triples:
            unique_triples.add(tuple(valid_triple))
            valid_triples.append(valid_triple)

    return valid_triples

# Strategy for generating triples
def triple_strategy():
    return st.lists(
        st.one_of([
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            st.just(""),  # Empty string
            st.integers(),  # Non-string values
            st.floats(allow_nan=False, allow_infinity=False),
            st.booleans()
        ]),
        min_size=3, max_size=3
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(triples=st.lists(triple_strategy(), min_size=0, max_size=20))
@example(triples=[])
@example(triples=[["a", "b", "c"]])
@example(triples=[["", "b", "c"]])
@example(triples=[["a", "", "c"]])
@example(triples=[["a", "b", ""]])
@example(triples=[["a", "b", "c"], ["a", "b", "c"]])  # Duplicate
@example(triples=[[1, "b", "c"]])  # Non-string value
@example(triples=[["a", "b", "c", "d"]])  # Invalid length
def test_filter_invalid_triples(triples: List[List[str]]):
    global stop_collecting
    if stop_collecting:
        return
    
    triples_copy = copy.deepcopy(triples)
    try:
        expected = _filter_invalid_triples(triples_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter cases to prioritize meaningful branches
    if any(
        len(triple) != 3 or
        (not isinstance(triple[0], str) or triple[0].strip() == "") or
        (not isinstance(triple[1], str) or triple[1].strip() == "") or
        (not isinstance(triple[2], str) or triple[2].strip() == "")
        for triple in triples
    ) or any(triple != ["a", "b", "c"] for triple in triples):
        generated_cases.append({
            "Inputs": {"triples": triples},
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