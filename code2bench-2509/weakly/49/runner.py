import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import normalize_run_path as func1
from urllib.parse import urlparse
from typing import Optional, Tuple

# Ground truth function (func0), keep its original implementation and name
def normalize_run_path(target: str, entity: Optional[str], project: Optional[str]) -> Tuple[str, str, str]:
    if target.startswith(("http://", "https://")):
        parsed = urlparse(target)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 3:
            raise ValueError(f"Could not parse run information from URL: {target}")
        entity = parts[0]
        project = parts[1]
        if parts[2] == "runs" and len(parts) >= 4:
            run_id = parts[3]
        else:
            run_id = parts[2]
        return entity, project, run_id

    parts = [p for p in target.split("/") if p]
    if len(parts) == 1:
        if not entity or not project:
            raise ValueError("Bare run ids require --entity and --project.")
        return entity, project, parts[0]

    if len(parts) >= 3:
        entity = parts[0]
        project = parts[1]
        if parts[2] == "runs" and len(parts) >= 4:
            run_id = parts[3]
        else:
            run_id = parts[2]
        return entity, project, run_id

    raise ValueError(f"Unrecognized run target: {target}")

# Compare outputs
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            target = inputs["target"]
            entity = inputs["entity"]
            project = inputs["project"]

            try:
                expected_output = normalize_run_path(target, entity, project)
                actual_output = func1(target, entity, project)

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