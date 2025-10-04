from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import csv
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

# Strategies for generating inputs
def eval_type_strategy():
    return st.sampled_from(["seceval", "cybermetric", "cti_bench"])

def dataset_file_strategy(eval_type):
    if eval_type == "seceval":
        return st.builds(
            lambda x: "seceval.json",
            st.lists(
                st.fixed_dictionaries({
                    "question": st.text(min_size=1, max_size=50),
                    "choices": st.lists(st.text(min_size=1, max_size=20), min_size=1, max_size=5),
                    "answer": st.text(min_size=1, max_size=20)
                }),
                min_size=1, max_size=5
            ).map(lambda x: json.dump(x, open("seceval.json", "w")))
        )
    elif eval_type == "cybermetric":
        return st.builds(
            lambda x: "cybermetric.json",
            st.fixed_dictionaries({
                "questions": st.lists(
                    st.fixed_dictionaries({
                        "question": st.text(min_size=1, max_size=50),
                        "answers": st.dictionaries(st.text(min_size=1, max_size=10), st.text(min_size=1, max_size=20), min_size=1, max_size=5),
                        "solution": st.text(min_size=1, max_size=20)
                    }),
                    min_size=1, max_size=5
                )
            }).map(lambda x: json.dump(x, open("cybermetric.json", "w")))
        )
    elif eval_type == "cti_bench":
        return st.builds(
            lambda x: "cti_bench.tsv",
            st.lists(
                st.one_of(
                    st.tuples(
                        st.text(min_size=1, max_size=20),
                        st.text(min_size=1, max_size=50),
                        st.text(min_size=1, max_size=20),
                        st.text(min_size=1, max_size=20),
                        st.text(min_size=1, max_size=20),
                        st.text(min_size=1, max_size=20),
                        st.text(min_size=1, max_size=50),
                        st.text(min_size=1, max_size=20)
                    ),
                    st.tuples(
                        st.text(min_size=1, max_size=20),
                        st.text(min_size=1, max_size=20),
                        st.text(min_size=1, max_size=50),
                        st.text(min_size=1, max_size=50),
                        st.text(min_size=1, max_size=20)
                    ),
                    st.tuples(
                        st.text(min_size=1, max_size=20),
                        st.text(min_size=1, max_size=50),
                        st.text(min_size=1, max_size=50),
                        st.text(min_size=1, max_size=20)
                    )
                ),
                min_size=1, max_size=5
            ).map(lambda x: "\n".join(["\t".join(row) for row in x])).map(lambda x: open("cti_bench.tsv", "w").write(x))
        )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    eval_type=eval_type_strategy(),
    dataset_file=st.builds(
        lambda x: dataset_file_strategy(x),
        eval_type_strategy()
    )
)
@example(eval_type="seceval", dataset_file="seceval.json")
@example(eval_type="cybermetric", dataset_file="cybermetric.json")
@example(eval_type="cti_bench", dataset_file="cti_bench.tsv")
def test_load_dataset(eval_type: str, dataset_file: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    eval_type_copy = copy.deepcopy(eval_type)
    dataset_file_copy = copy.deepcopy(dataset_file)

    # Call func0 to verify input validity
    try:
        expected = load_dataset(dataset_file_copy, eval_type_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "dataset_file": dataset_file_copy,
            "eval_type": eval_type_copy
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