from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List, Tuple
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
def _parse_n_check_triples(triples_str: str) -> List[Tuple[str, str, str]]:
    processed = []
    split_by_newline = triples_str.split("\n")
    if len(split_by_newline) > 1:
        split_triples = split_by_newline
        llm_obeyed = True
    else:
        split_triples = triples_str[1:-1].split(") (")
        llm_obeyed = False
    for triple_str in split_triples:
        try:
            if llm_obeyed:
                triple_str = triple_str.replace("(", "").replace(")", "").replace("'", "")
            split_trip = triple_str.split(',')
            split_trip = [(i[1:] if i[0] == " " else i) for i in split_trip]
            split_trip = [(i[:-1].lower() if i[-1] == " " else i) for i in split_trip]
            potential_trip = tuple(split_trip)
        except:
            continue
        if 'tuple' in str(type(potential_trip)) and len(potential_trip) == 3 and "note:" not in potential_trip[0].lower():
            if potential_trip[0] != '' and potential_trip[1] != '' and potential_trip[2] != '':
                processed.append(potential_trip)
    return processed

# Strategy for generating triples strings
def triples_strategy():
    # Strategy for individual triples
    triple_strategy = st.tuples(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    )
    
    # Strategy for multiple triples
    return st.one_of([
        # Format: "(e, r, e) (e, r, e) ... (e, r, e)"
        st.lists(triple_strategy, min_size=1, max_size=5).map(
            lambda triples: " ".join(f"({t[0]}, {t[1]}, {t[2]})" for t in triples)
        ),
        # Format: "(e, r, e)\n(e, r, e)\n...\n(e, r, e)"
        st.lists(triple_strategy, min_size=1, max_size=5).map(
            lambda triples: "\n".join(f"({t[0]}, {t[1]}, {t[2]})" for t in triples)
        ),
        # Format with single quotes: "('e', 'r', 'e') ('e', 'r', 'e') ... ('e', 'r', 'e')"
        st.lists(triple_strategy, min_size=1, max_size=5).map(
            lambda triples: " ".join(f"('{t[0]}', '{t[1]}', '{t[2]}')" for t in triples)
        ),
        # Format with single quotes and newlines: "('e', 'r', 'e')\n('e', 'r', 'e')\n...\n('e', 'r', 'e')"
        st.lists(triple_strategy, min_size=1, max_size=5).map(
            lambda triples: "\n".join(f"('{t[0]}', '{t[1]}', '{t[2]}')" for t in triples)
        ),
        # Invalid formats
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100).map(
            lambda s: s.replace(",", " ").replace("(", " ").replace(")", " ")
        )
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(triples_str=triples_strategy())
@example(triples_str="(e1, r1, e2) (e3, r2, e4)")
@example(triples_str="(e1, r1, e2)\n(e3, r2, e4)")
@example(triples_str="('e1', 'r1', 'e2') ('e3', 'r2', 'e4')")
@example(triples_str="('e1', 'r1', 'e2')\n('e3', 'r2', 'e4')")
@example(triples_str="( , , )")
@example(triples_str="(e1, r1, e2) ( , , )")
@example(triples_str="note: (e1, r1, e2)")
def test_parse_n_check_triples(triples_str: str):
    global stop_collecting
    if stop_collecting:
        return
    
    triples_str_copy = copy.deepcopy(triples_str)
    try:
        expected = _parse_n_check_triples(triples_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"triples_str": triples_str},
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