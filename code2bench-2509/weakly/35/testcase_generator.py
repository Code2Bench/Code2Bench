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
def get_changed_lines_from_file(diff_txt_path):
    """Parse diff.txt to get changed lines per file"""
    file_changes = defaultdict(set)
    current_file = None

    with open(diff_txt_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("+++ b/"):
                current_file = line[6:].strip()
            elif line.startswith("@@"):
                match = re.search(r"\+(\d+)(?:,(\d+))?", line)
                if match and current_file:
                    start_line = int(match.group(1))
                    line_count = int(match.group(2) or "1")
                    for i in range(start_line, start_line + line_count):
                        file_changes[current_file].add(i)
    return file_changes

# Strategy for generating diff.txt content
def diff_txt_strategy():
    # Generate file paths
    file_path = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P'), whitelist_characters='./_'),
        min_size=1, max_size=20
    ).map(lambda s: s.strip())

    # Generate line numbers and counts
    line_number = st.integers(min_value=1, max_value=1000)
    line_count = st.integers(min_value=1, max_value=10)

    # Generate diff lines
    diff_line = st.builds(
        lambda f, ln, lc: f"+++ b/{f}\n@@ -0,0 +{ln},{lc} @@\n",
        file_path, line_number, line_count
    )

    # Generate multiple diff sections
    return st.lists(
        diff_line,
        min_size=1, max_size=5
    ).map(lambda x: ''.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(diff_txt=diff_txt_strategy())
@example(diff_txt="+++ b/file1.txt\n@@ -0,0 +1,1 @@\n")
@example(diff_txt="+++ b/file2.txt\n@@ -0,0 +10,5 @@\n")
@example(diff_txt="+++ b/file3.txt\n@@ -0,0 +100,10 @@\n")
@example(diff_txt="+++ b/file4.txt\n@@ -0,0 +1,1 @@\n+++ b/file5.txt\n@@ -0,0 +2,3 @@\n")
def test_get_changed_lines_from_file(diff_txt: str):
    global stop_collecting
    if stop_collecting:
        return

    # Create a temporary file with the generated diff content
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(diff_txt)
        diff_txt_path = f.name

    # Deep copy input to avoid modification
    diff_txt_path_copy = copy.deepcopy(diff_txt_path)

    # Call func0 to verify input validity
    try:
        expected = get_changed_lines_from_file(diff_txt_path_copy)
    except Exception:
        os.unlink(diff_txt_path)
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "diff_txt_path": diff_txt_path_copy
        }
    })

    # Clean up temporary file
    os.unlink(diff_txt_path)

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)