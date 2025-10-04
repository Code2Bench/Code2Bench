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
def parse_lcov(outputs: List[str]):
    switch, extracted_outputs = False, []
    for line in outputs:
        if switch == False and "tmp_src" in line:
            switch = True
        if switch == True and "end_of_record" in line:
            switch = False
        if switch:
            extracted_outputs.append(line)

    branch, branch_covered = [], []
    for line in extracted_outputs:
        if line.startswith("BRDA"):
            # BRDA format: BR:<lineno>,<blockno>,<branchno>,<taken>
            lineno, blockno, branchno, taken = line[5:].split(",")
            branch_sig = f"BR:{lineno},{blockno},{branchno}"
            branch.append(branch_sig)
            if taken not in ["0", "-"]:
                branch_covered.append(branch_sig)
    per = 1.0 if len(branch) == 0 else len(branch_covered) / len(branch)
    return per, branch, branch_covered

# Strategy for generating LCOV-like lines
def lcov_line_strategy():
    return st.one_of([
        # Lines containing "tmp_src"
        st.just("tmp_src"),
        # Lines containing "end_of_record"
        st.just("end_of_record"),
        # BRDA lines
        st.tuples(
            st.integers(min_value=1, max_value=1000),
            st.integers(min_value=1, max_value=100),
            st.integers(min_value=1, max_value=100),
            st.one_of([st.just("0"), st.just("-"), st.just("1")])
        ).map(lambda x: f"BRDA:{x[0]},{x[1]},{x[2]},{x[3]}"),
        # Generic lines
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(outputs=st.lists(lcov_line_strategy(), min_size=1, max_size=20))
@example(outputs=["tmp_src", "BRDA:1,1,1,1", "end_of_record"])
@example(outputs=["tmp_src", "BRDA:1,1,1,0", "end_of_record"])
@example(outputs=["tmp_src", "BRDA:1,1,1,-", "end_of_record"])
@example(outputs=["tmp_src", "BRDA:1,1,1,1", "BRDA:1,1,2,0", "end_of_record"])
@example(outputs=["tmp_src", "BRDA:1,1,1,1", "BRDA:1,1,2,1", "end_of_record"])
@example(outputs=["tmp_src", "end_of_record"])
@example(outputs=["tmp_src", "BRDA:1,1,1,1", "BRDA:1,1,2,1", "BRDA:1,1,3,1", "end_of_record"])
def test_parse_lcov(outputs: List[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    outputs_copy = copy.deepcopy(outputs)
    try:
        expected = parse_lcov(outputs_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any("tmp_src" in line for line in outputs) or any("BRDA" in line for line in outputs):
        generated_cases.append({
            "Inputs": {"outputs": outputs},
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