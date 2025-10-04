import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import normalize_unicode_homographs as func1
import unicodedata

# Ground truth function (func0), keep its original implementation and name
def normalize_unicode_homographs(text: str) -> str:
    homograph_map = {
        '\u0430': 'a',  # Cyrillic а
        '\u0435': 'e',  # Cyrillic е  
        '\u043e': 'o',  # Cyrillic о
        '\u0440': 'p',  # Cyrillic р
        '\u0441': 'c',  # Cyrillic с
        '\u0443': 'y',  # Cyrillic у
        '\u0445': 'x',  # Cyrillic х
        '\u0410': 'A',  # Cyrillic А
        '\u0415': 'E',  # Cyrillic Е
        '\u041e': 'O',  # Cyrillic О
        '\u0420': 'P',  # Cyrillic Р
        '\u0421': 'C',  # Cyrillic С
        '\u0425': 'X',  # Cyrillic Х
        '\u03b1': 'a',  # Greek α
        '\u03bf': 'o',  # Greek ο
        '\u03c1': 'p',  # Greek ρ
        '\u03c5': 'u',  # Greek υ
        '\u03c7': 'x',  # Greek χ
        '\u0391': 'A',  # Greek Α
        '\u039f': 'O',  # Greek Ο
        '\u03a1': 'P',  # Greek Ρ
        '\u2010': '-',  # Hyphen
        '\u2011': '-',  # Non-breaking hyphen
        '\u2212': '-',  # Minus sign
        '\uff0d': '-',  # Fullwidth hyphen-minus
    }
    normalized = text
    for homograph, replacement in homograph_map.items():
        normalized = normalized.replace(homograph, replacement)
    normalized = unicodedata.normalize('NFKD', normalized)
    return normalized

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
            text = inputs["text"]

            try:
                expected_output = normalize_unicode_homographs(text)
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
        print("No test cases found.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)