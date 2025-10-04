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
def calculate_avg_pass_at_3(query_results):
    round_names = ["round1", "round2", "round3"]
    total_correct = {round_name: 0 for round_name in round_names}

    for query, results in query_results.items():  
        for round_name in round_names:  
            if results[round_name] == "Correct":
                total_correct[round_name] += 1 

    avg_overall = sum(total_correct[r] / len(query_results) for r in round_names) / len(round_names)

    return round(avg_overall * 100, 2)

# Strategy for generating query_results
def query_results_strategy():
    round_names = ["round1", "round2", "round3"]
    return st.dictionaries(
        keys=st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('L', 'N'))),
        values=st.fixed_dictionaries({
            round_name: st.one_of([st.just("Correct"), st.just("Incorrect")]) for round_name in round_names
        }),
        min_size=1,
        max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(query_results=query_results_strategy())
@example(query_results={"query1": {"round1": "Correct", "round2": "Correct", "round3": "Correct"}})
@example(query_results={"query1": {"round1": "Incorrect", "round2": "Incorrect", "round3": "Incorrect"}})
@example(query_results={"query1": {"round1": "Correct", "round2": "Incorrect", "round3": "Correct"}})
@example(query_results={"query1": {"round1": "Correct", "round2": "Correct", "round3": "Incorrect"},
                        "query2": {"round1": "Incorrect", "round2": "Correct", "round3": "Correct"}})
def test_calculate_avg_pass_at_3(query_results):
    global stop_collecting
    if stop_collecting:
        return
    
    query_results_copy = copy.deepcopy(query_results)
    try:
        expected = calculate_avg_pass_at_3(query_results_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"query_results": query_results},
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