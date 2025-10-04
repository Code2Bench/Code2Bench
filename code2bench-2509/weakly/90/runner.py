import json
import copy
from typing import Any
from helper import deep_compare, load_test_cases_from_json
from tested import _clean_text_value as func1

# Ground truth function (func0), keep its original implementation and name
def _clean_text_value(value: Any) -> Any:
    """Fix common text encoding issues and decode escaped sequences.

    - Fix UTF-8 displayed as Windows-1252/latin-1 (e.g., â -> ’)
    - Decode backslash-escaped unicode sequences when present
    - Leave non-strings unchanged
    """
    if not isinstance(value, str):
        return value

    text = value

    # Attempt to fix mojibake: bytes intended as UTF-8 shown as latin-1
    # Trigger only if typical mojibake markers present
    if any(mark in text for mark in ("â€", "Ã", "Â")):
        try:
            text = text.encode("latin-1", errors="ignore").decode(
                "utf-8", errors="ignore"
            )
        except Exception:
            pass

    # Decode literal escape sequences like \u2019 -> ’ if present
    if "\\u" in text or "\\x" in text:
        try:
            text = codecs.decode(text.encode("utf-8"), "unicode_escape")
        except Exception:
            pass

    return text

# Compare outputs function
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
            value = inputs["value"]

            try:
                expected_output = _clean_text_value(value)
                actual_output = func1(value)

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