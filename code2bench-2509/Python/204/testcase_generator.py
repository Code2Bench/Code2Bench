from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List, Dict, Tuple, Optional, Any
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
def _extract_table(content: List[str], start_idx: int) -> Tuple[Optional[Dict[str, Any]], int]:
    if start_idx >= len(content):
        return None, 0

    table_lines = []
    i = start_idx

    while i < len(content) and content[i].strip() and '|' in content[i]:
        table_lines.append(content[i].strip())
        i += 1

    if len(table_lines) < 2:
        return None, 1

    header_line = table_lines[0]
    headers = [h.strip() for h in header_line.split('|') if h.strip()]

    data_start_idx = 1
    if len(table_lines) > 1 and all(c in '-|: ' for c in table_lines[1]):
        data_start_idx = 2

    rows = []
    for line in table_lines[data_start_idx:]:
        if '|' in line:
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if len(cells) == len(headers):
                rows.append(cells)

    consumed_lines = len(table_lines)

    if headers and rows:
        return {
            'headers': headers,
            'rows': rows
        }, consumed_lines

    return None, consumed_lines

# Strategy for generating table-like content
def table_line_strategy():
    return st.one_of([
        # Header line
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just('|'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just('|'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: ' '.join(x)),
        # Separator line
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), min_size=1, max_size=10),
            st.just('|'),
            st.text(st.characters(whitelist_categories=('Zs',)), min_size=1, max_size=10),
            st.just('|'),
            st.text(st.characters(whitelist_categories=('Zs',)), min_size=1, max_size=10)
        ).map(lambda x: '-'.join(x)),
        # Data line
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just('|'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just('|'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: ' '.join(x)),
        # Empty line
        st.just('')
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    content=st.lists(table_line_strategy(), min_size=0, max_size=20),
    start_idx=st.integers(min_value=0)
)
@example(content=["Header1 | Header2 | Header3", "--- | --- | ---", "Data1 | Data2 | Data3"], start_idx=0)
@example(content=["Header1 | Header2 | Header3", "Data1 | Data2 | Data3"], start_idx=0)
@example(content=["Header1 | Header2 | Header3"], start_idx=0)
@example(content=["Header1 | Header2 | Header3", "--- | --- | ---"], start_idx=0)
@example(content=["Header1 | Header2 | Header3", "--- | --- | ---", "Data1 | Data2 | Data3", "Data4 | Data5 | Data6"], start_idx=0)
@example(content=["Header1 | Header2 | Header3", "--- | --- | ---", "Data1 | Data2 | Data3", "Data4 | Data5 | Data6"], start_idx=1)
@example(content=["Header1 | Header2 | Header3", "--- | --- | ---", "Data1 | Data2 | Data3", "Data4 | Data5 | Data6"], start_idx=2)
@example(content=["Header1 | Header2 | Header3", "--- | --- | ---", "Data1 | Data2 | Data3", "Data4 | Data5 | Data6"], start_idx=3)
@example(content=["Header1 | Header2 | Header3", "--- | --- | ---", "Data1 | Data2 | Data3", "Data4 | Data5 | Data6"], start_idx=4)
@example(content=["Header1 | Header2 | Header3", "--- | --- | ---", "Data1 | Data2 | Data3", "Data4 | Data5 | Data6"], start_idx=5)
def test_extract_table(content: List[str], start_idx: int):
    global stop_collecting
    if stop_collecting:
        return
    
    content_copy = copy.deepcopy(content)
    try:
        expected, consumed_lines = _extract_table(content_copy, start_idx)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if expected is not None or consumed_lines > 0:
        generated_cases.append({
            "Inputs": {"content": content, "start_idx": start_idx},
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