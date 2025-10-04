import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import load_dataset as func1

# Ground truth function (func0), keep its original implementation and name
def load_dataset(dataset_file, eval_type):
    questions = [] #list of questions: {question: str, answers: dict, solution: str}
    if eval_type == "seceval":
        with open(dataset_file, 'r') as f:
            data = json.load(f)
            for question in data:
                questions.append({
                    "Question": question["question"],
                    "Choices": "\n".join(question["choices"]),
                    "Solution": question["answer"]
                })

    elif eval_type == "cybermetric":
        with open(dataset_file, 'r') as f:
            data = json.load(f)
            for question in data.get("questions", []):
                questions.append({
                    "Question": question.get("question", ""),
                    "Choices": "\n".join([f"{k}: {v}" for k, v in question.get("answers", {}).items()]),
                    "Solution": question.get("solution", "")
                })
    elif eval_type == "cti_bench":
        with open(dataset_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader, None)
            for row in reader:
                # Handle three possible formats:
                # Format 1: [URL, Question, Option A, Option B, Option C, Option D, Prompt, GT] (8 columns)
                # Format 2: [URL, Platform, Description, Prompt, GT] (5 columns)
                # Format 3: [URL, Description, Prompt, GT] (4 columns)

                if len(row) == 8:
                    # MCQ format
                    questions.append({
                        "Question": row[1],
                        "Choices": f"A: {row[2]}\nB: {row[3]}\nC: {row[4]}\nD: {row[5]}",
                        "Solution": row[7]
                    })
                elif len(row) == 5:
                    # ATE format (no choices, just open-ended)
                    questions.append({
                        "Question": row[2] + row[3],  # Description + Prompt
                        "Choices": "",       # No choices for ATE
                        "Solution": row[4]   # GT
                    })
                elif len(row) == 4:
                    # RCM format: [URL, Description, Prompt, GT]
                    questions.append({
                        "Question": row[1] + row[2],  # Description + Prompt
                        "Choices": "",       # No choices for RCM
                        "Solution": row[3]   # GT
                    })

    return questions

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
            dataset_file = inputs["dataset_file"]
            eval_type = inputs["eval_type"]

            try:
                expected_output = load_dataset(dataset_file, eval_type)
                actual_output = func1(dataset_file, eval_type)

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