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
def extract_locs_for_files(locs, file_names, keep_old_order=False):
    if keep_old_order:
        results = {fn: [] for fn in file_names}
    else:
        results = {}  # dict is insertion ordered
    current_file_name = None
    for loc in locs:
        for line in loc.splitlines():
            if line.strip().endswith('.py'):
                current_file_name = line.strip()
            elif line.strip() and any(
                line.startswith(w) for w in ['line:', 'function:', 'class:', 'variable:']
            ):
                if current_file_name in file_names:
                    if current_file_name not in results:
                        results[current_file_name] = []
                    results[current_file_name].append(line)
                else:
                    pass

    for file_name in file_names:
        if file_name not in results:  # guard for new order case
            results[file_name] = []

    return {fn: ['\n'.join(results[fn])] for fn in results.keys()}

# Strategy for generating file names
def file_name_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=20).map(lambda s: s + '.py')

# Strategy for generating lines
def line_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=50).map(lambda s: 'line: ' + s),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=50).map(lambda s: 'function: ' + s),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=50).map(lambda s: 'class: ' + s),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=50).map(lambda s: 'variable: ' + s),
        file_name_strategy()
    ])

# Strategy for generating locs
def locs_strategy():
    return st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=100), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    locs=locs_strategy(),
    file_names=st.lists(file_name_strategy(), min_size=1, max_size=5, unique=True),
    keep_old_order=st.booleans()
)
@example(locs=["file1.py\nline: 1"], file_names=["file1.py"], keep_old_order=True)
@example(locs=["file1.py\nline: 1"], file_names=["file1.py"], keep_old_order=False)
@example(locs=["file1.py\nline: 1\nfile2.py\nline: 2"], file_names=["file1.py", "file2.py"], keep_old_order=True)
@example(locs=["file1.py\nline: 1\nfile2.py\nline: 2"], file_names=["file1.py", "file2.py"], keep_old_order=False)
@example(locs=["file1.py\nline: 1\nfile2.py\nline: 2"], file_names=["file3.py"], keep_old_order=True)
@example(locs=["file1.py\nline: 1\nfile2.py\nline: 2"], file_names=["file3.py"], keep_old_order=False)
@example(locs=["file1.py\nline: 1\nfile2.py\nline: 2"], file_names=[], keep_old_order=True)
@example(locs=["file1.py\nline: 1\nfile2.py\nline: 2"], file_names=[], keep_old_order=False)
def test_extract_locs_for_files(locs, file_names, keep_old_order):
    global stop_collecting
    if stop_collecting:
        return
    
    locs_copy = copy.deepcopy(locs)
    file_names_copy = copy.deepcopy(file_names)
    try:
        expected = extract_locs_for_files(locs_copy, file_names_copy, keep_old_order)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"locs": locs, "file_names": file_names, "keep_old_order": keep_old_order},
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