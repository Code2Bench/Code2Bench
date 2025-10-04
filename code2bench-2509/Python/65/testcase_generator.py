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
def parse_evolve_blocks(code: str) -> List[Tuple[int, int, str]]:
    """
    Parse evolve blocks from code

    Args:
        code: Source code with evolve blocks

    Returns:
        List of tuples (start_line, end_line, block_content)
    """
    lines = code.split("\n")
    blocks = []

    in_block = False
    start_line = -1
    block_content = []

    for i, line in enumerate(lines):
        if "# EVOLVE-BLOCK-START" in line:
            in_block = True
            start_line = i
            block_content = []
        elif "# EVOLVE-BLOCK-END" in line and in_block:
            in_block = False
            blocks.append((start_line, i, "\n".join(block_content)))
        elif in_block:
            block_content.append(line)

    return blocks

# Strategy for generating code-like lines
def code_line_strategy():
    return st.one_of([
        st.just("# EVOLVE-BLOCK-START"),
        st.just("# EVOLVE-BLOCK-END"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(code=st.lists(code_line_strategy(), min_size=1, max_size=20).map(lambda x: "\n".join(x)))
@example(code="# EVOLVE-BLOCK-START\n# EVOLVE-BLOCK-END")
@example(code="# EVOLVE-BLOCK-START\nline1\nline2\n# EVOLVE-BLOCK-END")
@example(code="line1\n# EVOLVE-BLOCK-START\nline2\n# EVOLVE-BLOCK-END\nline3")
@example(code="# EVOLVE-BLOCK-START\nline1\n# EVOLVE-BLOCK-START\nline2\n# EVOLVE-BLOCK-END\nline3\n# EVOLVE-BLOCK-END")
@example(code="# EVOLVE-BLOCK-START\nline1\n# EVOLVE-BLOCK-END\n# EVOLVE-BLOCK-START\nline2\n# EVOLVE-BLOCK-END")
def test_parse_evolve_blocks(code: str):
    global stop_collecting
    if stop_collecting:
        return
    
    code_copy = copy.deepcopy(code)
    try:
        expected = parse_evolve_blocks(code_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "# EVOLVE-BLOCK-START" in code and "# EVOLVE-BLOCK-END" in code:
        generated_cases.append({
            "Inputs": {"code": code},
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