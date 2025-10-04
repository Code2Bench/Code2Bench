import json
import copy
from datetime import datetime
from typing import Any
from helper import deep_compare, load_test_cases_from_json
from tested import _prepare_node_metadata as func1

# Ground truth function (func0), keep its original implementation and name
def _prepare_node_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Ensure metadata has proper datetime fields and normalized types.

    - Fill `created_at` and `updated_at` if missing (in ISO 8601 format).
    - Convert embedding to list of float if present.
    """
    now = datetime.utcnow().isoformat()

    # Fill timestamps if missing
    metadata.setdefault("created_at", now)
    metadata.setdefault("updated_at", now)

    # Normalize embedding type
    embedding = metadata.get("embedding")
    if embedding and isinstance(embedding, list):
        metadata["embedding"] = [float(x) for x in embedding]

    return metadata

# Define compare_outputs function
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
            metadata = inputs["metadata"]

            try:
                expected_output = _prepare_node_metadata(metadata)
                actual_output = func1(metadata)

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
    if not test_cases:
        print("No test cases loaded. Exiting.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)