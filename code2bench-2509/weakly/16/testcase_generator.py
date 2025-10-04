from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
from collections import defaultdict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def extract_error_files(output):
    error_files = defaultdict(list)
    error_pattern = r'❌\s+([^:]+):\s*(.+)'
    lines = output.split('\n')
    for line in lines:
        match = re.match(error_pattern, line.strip())
        if match:
            file_path = match.group(1).strip()
            error_msg = match.group(2).strip()
            error_files[file_path].append(error_msg)
    return error_files

# Strategy for generating output text
def output_strategy():
    # Generate file paths
    file_path = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P'), whitelist_characters='./_'),
        min_size=1, max_size=20
    )
    
    # Generate error messages
    error_msg = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1, max_size=50
    )
    
    # Combine into error lines
    error_line = st.builds(
        lambda f, e: f"❌ {f}: {e}",
        file_path, error_msg
    )
    
    # Mix error lines with random lines
    return st.lists(
        st.one_of(
            error_line,
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=50)
        ),
        min_size=0, max_size=10
    ).map(lambda x: '\n'.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(output=output_strategy())
@example(output="")
@example(output="❌ file1.txt: Error message 1")
@example(output="❌ file1.txt: Error message 1\n❌ file2.txt: Error message 2")
@example(output="❌ file1.txt: Error message 1\nRandom line\n❌ file2.txt: Error message 2")
@example(output="Random line 1\nRandom line 2")
def test_extract_error_files(output: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    output_copy = copy.deepcopy(output)

    # Call func0 to verify input validity
    try:
        expected = extract_error_files(output_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "output": output_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)