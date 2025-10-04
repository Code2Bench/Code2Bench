import json
import os
import copy
import re
import html
from helper import deep_compare
from tested import sanitize_html as func1

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth function
def sanitize_html(text: str) -> str:
    if not text:
        return ""

    # Convert text to string if it's not already
    text = str(text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Handle comparison operators that break MDX
    text = re.sub(r"<(\d+)", r"less than \1", text)
    text = re.sub(r">(\d+)", r"greater than \1", text)
    text = re.sub(r"<=(\d+)", r"less than or equal to \1", text)
    text = re.sub(r">=(\d+)", r"greater than or equal to \1", text)

    # For standalone < and > characters, replace with safer alternatives
    text = re.sub(r"(?<!\w)<(?!\w)", "&lt;", text)
    text = re.sub(r"(?<!\w)>(?!\w)", "&gt;", text)

    # Replace quote types that can break MDX
    text = text.replace("|", "\\|")
    text = re.sub(r"\{([^}]*)\s+([^}]*)\}", r"{\1_\2}", text)

    # Handle JSON examples with quotes
    if "{" in text and "}" in text:
        text = re.sub(
            r"(\{[^{}]*\})", lambda m: m.group(0).replace("'", "`").replace('"', "`"), text
        )
        text = re.sub(r"(\{[^{}]+\})", r"`\1`", text)

    # Handle special characters that might trigger MDX parsing
    text = text.replace("$", "\\$")
    text = text.replace("%", "\\%")

    # Some special HTML entities need to be preserved during unescaping
    text = html.unescape(text.replace("&lt;", "_LT_").replace("&gt;", "_GT_"))
    text = text.replace("_LT_", "&lt;").replace("_GT_", "&gt;")

    # Remove any trailing/leading whitespace
    text = text.strip()

    return text

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)
    return test_cases

def compare_outputs(expected, actual):
    # Use deep_compare for basic types (str in this case)
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner structure
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            text = inputs["text"]

            try:
                expected_output = sanitize_html(text)
                actual_output = func1(text)

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
        print("No test cases loaded.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)