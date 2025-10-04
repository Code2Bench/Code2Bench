import json
import copy
from typing import List, Dict, Any
from helper import deep_compare, load_test_cases_from_json
from tested import group_sse_events as func1
from collections import defaultdict
import re

# Ground truth function (func0), keep its original implementation and name
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

# Define compare_outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Define diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            sse_files = inputs["sse_files"]

            try:
                expected_output = group_sse_events(sse_files)
                actual_output = func1(sse_files)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output,
                        "actual": actual_output
                    })
            except Exception as e:
                failed_count += 1
                failures.append({
                    "case_id": i+1,
                    "type": "ExecutionError",
                    "inputs": inputs,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })

    except Exception as e:
        execution_error = {
            "type": "CriticalExecutionError",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }

    summary = {
        "passed": passed_count,
        "failed": failed_count,
        "total": len(test_cases),
        "failures": failures[:10],
        "execution_error": execution_error
    }

    print("\n---DIAGNOSTIC_SUMMARY_START---")
    print(json.dumps(summary, indent=2))
    print("---DIAGNOSTIC_SUMMARY_END---")

# Main block
if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    if test_cases:
        run_tests_with_loaded_cases_diagnostic(test_cases)
    else:
        print("No test cases found.")