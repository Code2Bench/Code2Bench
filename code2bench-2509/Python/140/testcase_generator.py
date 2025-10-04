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
def get_replaced_content(
    content: list[str],
    extras_list: list[str],
    start_line: str,
    end_line: str,
    prefix: str,
    suffix: str,
    add_empty_lines: bool,
) -> list[str]:
    result = []
    is_copying = True
    for line in content:
        if line.startswith(start_line):
            result.append(f"{line}")
            if add_empty_lines:
                result.append("\n")
            is_copying = False
            for extra in extras_list:
                result.append(f"{prefix}{extra}{suffix}\n")
        elif line.startswith(end_line):
            if add_empty_lines:
                result.append("\n")
            result.append(f"{line}")
            is_copying = True
        elif is_copying:
            result.append(line)
    return result

# Strategy for generating content lines
def content_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Strategy for generating extras_list
def extras_list_strategy():
    return st.lists(content_strategy(), min_size=0, max_size=5)

# Strategy for generating start_line and end_line
def marker_line_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)

# Strategy for generating prefix and suffix
def affix_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    content=st.lists(content_strategy(), min_size=0, max_size=10),
    extras_list=extras_list_strategy(),
    start_line=marker_line_strategy(),
    end_line=marker_line_strategy(),
    prefix=affix_strategy(),
    suffix=affix_strategy(),
    add_empty_lines=st.booleans()
)
@example(content=[], extras_list=[], start_line="start", end_line="end", prefix="", suffix="", add_empty_lines=False)
@example(content=["start", "line1", "end"], extras_list=["extra1"], start_line="start", end_line="end", prefix="[", suffix="]", add_empty_lines=True)
@example(content=["start", "line1", "end"], extras_list=[], start_line="start", end_line="end", prefix="", suffix="", add_empty_lines=False)
@example(content=["line1", "start", "line2", "end", "line3"], extras_list=["extra1", "extra2"], start_line="start", end_line="end", prefix="(", suffix=")", add_empty_lines=True)
@example(content=["start", "end"], extras_list=["extra1"], start_line="start", end_line="end", prefix="", suffix="", add_empty_lines=False)
def test_get_replaced_content(content, extras_list, start_line, end_line, prefix, suffix, add_empty_lines):
    global stop_collecting
    if stop_collecting:
        return
    
    content_copy = copy.deepcopy(content)
    extras_list_copy = copy.deepcopy(extras_list)
    try:
        expected = get_replaced_content(content_copy, extras_list_copy, start_line, end_line, prefix, suffix, add_empty_lines)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(line.startswith(start_line) or line.startswith(end_line) for line in content) or extras_list:
        generated_cases.append({
            "Inputs": {
                "content": content,
                "extras_list": extras_list,
                "start_line": start_line,
                "end_line": end_line,
                "prefix": prefix,
                "suffix": suffix,
                "add_empty_lines": add_empty_lines
            },
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