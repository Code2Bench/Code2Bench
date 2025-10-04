from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
from typing import Any, Dict, List
from collections import defaultdict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def group_sse_events(sse_files: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group SSE event files by trace ID and sort by sequence number."""
    trace_groups = defaultdict(list)

    for file_info in sse_files:
        trace_id = None
        sequence = None

        if file_info.get("is_local", True):
            # local pattern: {trace_id}_{timestamp}-sse_events_{sequence}.json
            filename = file_info["name"]
            match = re.match(r"([a-f0-9_]+)-sse_events_(\d+)\.json", filename)
            if match:
                trace_id, sequence = match.groups()
        else:
            # s3 pattern: app-{app_id}.req-{req_id}_{timestamp}/sse_events/{sequence}.json
            path = file_info["path"]
            match = re.match(r"(app-[a-f0-9-]+\.req-[a-f0-9-]+)_\d+/sse_events/(\d+)\.json", path)
            if match:
                trace_id, sequence = match.groups()
                # trace_id now has timestamp stripped (app-xxx.req-xxx)

        if trace_id and sequence is not None:
            file_info["trace_id"] = trace_id
            file_info["sequence"] = int(sequence)
            trace_groups[trace_id].append(file_info)

    # sort each group by sequence number (keep ALL events in sequence)
    for trace_id in trace_groups:
        trace_groups[trace_id].sort(key=lambda x: x["sequence"])

    return dict(trace_groups)

# Strategies for generating inputs
def trace_id_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_'),
        min_size=1, max_size=20
    )

def sequence_strategy():
    return st.integers(min_value=0, max_value=100)

def file_info_strategy():
    return st.builds(
        lambda is_local, name, path: {"is_local": is_local, "name": name, "path": path},
        is_local=st.booleans(),
        name=st.builds(
            lambda trace_id, sequence: f"{trace_id}-sse_events_{sequence}.json",
            trace_id=trace_id_strategy(),
            sequence=sequence_strategy()
        ),
        path=st.builds(
            lambda trace_id, sequence: f"app-{trace_id}.req-{trace_id}_1234567890/sse_events/{sequence}.json",
            trace_id=trace_id_strategy(),
            sequence=sequence_strategy()
        )
    )

def sse_files_strategy():
    return st.lists(file_info_strategy(), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(sse_files=sse_files_strategy())
@example(sse_files=[])
@example(sse_files=[{"is_local": True, "name": "trace1_1234567890-sse_events_0.json"}])
@example(sse_files=[{"is_local": False, "path": "app-123.req-456_1234567890/sse_events/0.json"}])
@example(sse_files=[
    {"is_local": True, "name": "trace1_1234567890-sse_events_0.json"},
    {"is_local": True, "name": "trace1_1234567890-sse_events_1.json"}
])
@example(sse_files=[
    {"is_local": False, "path": "app-123.req-456_1234567890/sse_events/0.json"},
    {"is_local": False, "path": "app-123.req-456_1234567890/sse_events/1.json"}
])
def test_group_sse_events(sse_files: List[Dict[str, Any]]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    sse_files_copy = copy.deepcopy(sse_files)

    # Call func0 to verify input validity
    try:
        expected = group_sse_events(sse_files_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "sse_files": sse_files_copy
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