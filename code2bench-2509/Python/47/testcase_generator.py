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
def remove_unindented_lines(
    code: str, protect_before: str, execeptions: list[str], trim_tails: list[str]
) -> str:
    lines = code.splitlines()
    cut_idx = []
    cut_enabled = False
    for i, line in enumerate(lines):
        if not cut_enabled and line.startswith(protect_before):
            cut_enabled = True
            continue
        if line.strip() == "":
            continue
        if any(line.startswith(e) for e in execeptions):
            continue

        lspace = len(line) - len(line.lstrip())
        if lspace == 0:
            cut_idx.append(i)

        if any(line.rstrip().startswith(t) for t in trim_tails):
            # cut off everything behind
            cut_idx.extend(list(range(i, len(lines))))
            break

    return "\n".join([line for i, line in enumerate(lines) if i not in cut_idx])

# Strategy for generating code-like lines
def line_strategy():
    return st.one_of([
        # Lines starting with protect_before
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1),
            st.one_of([st.just(":"), st.just(""), st.just(" # comment")])
        ).map(lambda x: "".join(x)),
        # Lines starting with exceptions
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1),
            st.one_of([st.just(":"), st.just(""), st.just(" # comment")])
        ).map(lambda x: "".join(x)),
        # Lines starting with trim_tails
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1),
            st.one_of([st.just(":"), st.just(""), st.just(" # comment")])
        ).map(lambda x: "".join(x)),
        # Empty lines
        st.just(""),
        # Generic code lines
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    code=st.lists(line_strategy(), min_size=1, max_size=20).map(lambda x: "\n".join(x)),
    protect_before=st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
    execeptions=st.lists(st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5), min_size=0, max_size=5),
    trim_tails=st.lists(st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5), min_size=0, max_size=5)
)
@example(code="def func():\n    pass", protect_before="def", execeptions=[], trim_tails=[])
@example(code="if condition:\n    value = 1", protect_before="if", execeptions=[], trim_tails=[])
@example(code="    previous_line\nnext_line", protect_before="previous", execeptions=[], trim_tails=[])
@example(code="previous_line,\nnext_line", protect_before="previous", execeptions=[], trim_tails=[])
@example(code="        value = 1", protect_before="value", execeptions=[], trim_tails=[])
@example(code="random_line", protect_before="random", execeptions=[], trim_tails=[])
def test_remove_unindented_lines(code: str, protect_before: str, execeptions: list[str], trim_tails: list[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    code_copy = copy.deepcopy(code)
    protect_before_copy = copy.deepcopy(protect_before)
    execeptions_copy = copy.deepcopy(execeptions)
    trim_tails_copy = copy.deepcopy(trim_tails)
    try:
        expected = remove_unindented_lines(code_copy, protect_before_copy, execeptions_copy, trim_tails_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(
        line.startswith(protect_before) or
        any(line.startswith(e) for e in execeptions) or
        any(line.rstrip().startswith(t) for t in trim_tails)
        for line in code.splitlines()
    ):
        generated_cases.append({
            "Inputs": {"code": code, "protect_before": protect_before, "execeptions": execeptions, "trim_tails": trim_tails},
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