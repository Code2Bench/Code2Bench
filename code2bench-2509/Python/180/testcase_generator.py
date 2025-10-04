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
def _parse_dos_filename(line):
    """Parse DOS 8.3 format filename from mdir output"""
    parts = line.split()
    if len(parts) < 1:
        return None, False

    is_directory = "<DIR>" in line.upper()
    if is_directory:
        return parts[0], True

    # For files: "FILENAME EXT SIZE DATE TIME"
    if (
        len(parts) >= 2
        and not parts[1].isdigit()
        and parts[1] not in ["bytes", "files"]
    ):
        return f"{parts[0]}.{parts[1]}", False
    return parts[0], False

# Strategy for generating DOS-like filenames
def dos_filename_strategy():
    return st.one_of([
        # Directory case
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=8),
            st.just("<DIR>")
        ).map(lambda x: f"{x[0]} {x[1]}"),
        # File case with extension
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=8),
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=3),
            st.integers(min_value=0, max_value=999999),
            st.dates(),
            st.times()
        ).map(lambda x: f"{x[0]} {x[1]} {x[2]} {x[3]} {x[4]}"),
        # File case without extension
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=8),
            st.integers(min_value=0, max_value=999999),
            st.dates(),
            st.times()
        ).map(lambda x: f"{x[0]} {x[1]} {x[2]} {x[3]}"),
        # Invalid case (bytes/files)
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=8),
            st.one_of([st.just("bytes"), st.just("files")]),
            st.integers(min_value=0, max_value=999999),
            st.dates(),
            st.times()
        ).map(lambda x: f"{x[0]} {x[1]} {x[2]} {x[3]} {x[4]}"),
        # Empty line
        st.just("")
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(line=dos_filename_strategy())
@example(line="FILENAME <DIR>")
@example(line="FILENAME EXT 12345 2023-01-01 12:00:00")
@example(line="FILENAME 12345 2023-01-01 12:00:00")
@example(line="FILENAME bytes 12345 2023-01-01 12:00:00")
@example(line="")
def test_parse_dos_filename(line):
    global stop_collecting
    if stop_collecting:
        return
    
    line_copy = copy.deepcopy(line)
    try:
        expected = _parse_dos_filename(line_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if len(line) > 0 or "<DIR>" in line.upper() or any(
        part.isdigit() or part in ["bytes", "files"]
        for part in line.split()
    ):
        generated_cases.append({
            "Inputs": {"line": line},
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