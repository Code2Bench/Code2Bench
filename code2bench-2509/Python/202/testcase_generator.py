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
def _parse_keywords_fallback(response: str) -> List[str]:
    keywords = []
    for line in response.strip().split("\n"):
        keyword = line.strip()
        keyword = keyword.lstrip("- *•").strip()
        if keyword and not keyword.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")):
            keyword = keyword.strip("\"'")
            if keyword:
                keywords.append(keyword)
    return keywords[:10]

# Strategy for generating response strings
def response_strategy():
    line_strategy = st.one_of([
        st.tuples(
            st.one_of([st.just("- "), st.just("* "), st.just("• "), st.just("")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
            st.one_of([st.just(""), st.just("'"), st.just('"')])
        ).map(lambda x: f"{x[0]}{x[1]}{x[2]}"),
        st.tuples(
            st.one_of([st.just("1."), st.just("2."), st.just("3."), st.just("4."), st.just("5."), st.just("6."), st.just("7."), st.just("8."), st.just("9."), st.just("10.")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
            st.one_of([st.just(""), st.just("'"), st.just('"')])
        ).map(lambda x: f"{x[0]} {x[1]}{x[2]}")
    ])
    return st.lists(line_strategy, min_size=1, max_size=20).map(lambda lines: "\n".join(lines))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(response=response_strategy())
@example(response="")
@example(response="keyword")
@example(response="- keyword")
@example(response="* keyword")
@example(response="• keyword")
@example(response="1. keyword")
@example(response="keyword 'quoted'")
@example(response="keyword \"quoted\"")
@example(response="keyword\n-keyword\n*keyword\n•keyword\n1. keyword")
def test_parse_keywords_fallback(response: str):
    global stop_collecting
    if stop_collecting:
        return
    
    response_copy = copy.deepcopy(response)
    try:
        expected = _parse_keywords_fallback(response_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(
        line.strip().lstrip("- *•").strip() and not line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10."))
        for line in response.strip().split("\n")
    ):
        generated_cases.append({
            "Inputs": {"response": response},
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