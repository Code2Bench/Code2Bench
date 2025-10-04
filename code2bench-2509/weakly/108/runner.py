import json
import copy
import ast
from helper import deep_compare, load_test_cases_from_json
from tested import scrape_python_blocks as func1

# Ground truth function (func0), keep its original implementation and name
def scrape_python_blocks(source_code, file_path_for_logging):
    """
    Parses Python source code from a string and extracts top-level classes,
    functions, and try/if blocks. It ignores methods inside classes and
    any blocks nested within functions.

    Args:
        source_code (str): The Python source code as a string.
        file_path_for_logging (str): The path of the file being scraped, for logging purposes.

    Returns:
        list: A list of strings, where each string is a source code block.
    """
    blocks = []
    try:
        # Parse the source code into an Abstract Syntax Tree (AST)
        tree = ast.parse(source_code, filename=file_path_for_logging)
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing {file_path_for_logging}: {e}")
        return []

    # Iterate over only the top-level nodes in the module's body
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Extracts top-level functions and full classes
            blocks.append(ast.get_source_segment(source_code, node))
        elif isinstance(node, ast.Try):
            # Extracts top-level try...except...finally blocks
            blocks.append(ast.get_source_segment(source_code, node))
        elif isinstance(node, ast.If):
            # Extracts top-level if blocks, as requested
            blocks.append(ast.get_source_segment(source_code, node))

    return blocks

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
            source_code = inputs["source_code"]
            file_path_for_logging = inputs["file_path_for_logging"]

            try:
                expected_output = scrape_python_blocks(source_code, file_path_for_logging)
                actual_output = func1(source_code, file_path_for_logging)

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