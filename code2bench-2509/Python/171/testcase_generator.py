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
def git_submodules_under_thirdparty(ls_stage_lines: list[str]) -> list[str]:
    """
    Use `git ls-files --stage` (mode 160000) and keep only those under thirdparty/.
    """
    names = []
    for line in ls_stage_lines:
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "160000":
            path = parts[3]  # repo-relative
            if path.startswith("thirdparty/"):
                rel = path[len("thirdparty/") :]
                first = rel.split("/", 1)[0]
                if first:
                    names.append(first)
    return sorted(set(names))

# Strategy for generating git ls-files --stage lines
def git_ls_stage_line_strategy():
    return st.one_of([
        # Valid lines with mode 160000 and path under thirdparty/
        st.tuples(
            st.just("160000"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10).map(lambda x: f"thirdparty/{x}")
        ).map(lambda x: " ".join(x)),
        # Valid lines with mode 160000 but path not under thirdparty/
        st.tuples(
            st.just("160000"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: " ".join(x)),
        # Invalid lines with incorrect mode
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=6),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: " ".join(x)),
        # Invalid lines with insufficient parts
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ls_stage_lines=st.lists(git_ls_stage_line_strategy(), min_size=0, max_size=20))
@example(ls_stage_lines=[])
@example(ls_stage_lines=["160000 abc def thirdparty/foo"])
@example(ls_stage_lines=["160000 abc def thirdparty/foo/bar"])
@example(ls_stage_lines=["160000 abc def thirdparty/"])
@example(ls_stage_lines=["160000 abc def otherpath/"])
@example(ls_stage_lines=["160000 abc def thirdparty/foo", "160000 abc def thirdparty/bar"])
@example(ls_stage_lines=["160000 abc def thirdparty/foo", "160000 abc def otherpath/bar"])
@example(ls_stage_lines=["160000 abc def thirdparty/foo", "160000 abc def thirdparty/foo"])
def test_git_submodules_under_thirdparty(ls_stage_lines: list[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    ls_stage_lines_copy = copy.deepcopy(ls_stage_lines)
    try:
        expected = git_submodules_under_thirdparty(ls_stage_lines_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(line.startswith("160000") and "thirdparty/" in line for line in ls_stage_lines):
        generated_cases.append({
            "Inputs": {"ls_stage_lines": ls_stage_lines},
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