from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import csv
import json
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
def load_benchmark_data(benchmark_file):
    """Load question-answer pairs from benchmark CSV"""
    benchmark_data = {}

    with open(benchmark_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question = row['question'].strip()
            answer = row['answer'].strip()
            benchmark_data[question] = answer

    return benchmark_data

# Strategy for generating CSV content
def csv_content_strategy():
    # Generate question-answer pairs with valid characters
    question = st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')))
    answer = st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')))
    return st.lists(
        st.tuples(question, answer),
        min_size=1, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(csv_content=csv_content_strategy())
@example(csv_content=[("Q1", "A1")])
@example(csv_content=[("Q1", "A1"), ("Q2", "A2")])
@example(csv_content=[("", "")])
def test_load_benchmark_data(csv_content):
    global stop_collecting
    if stop_collecting:
        return

    # Create a temporary CSV file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['question', 'answer'])
        writer.writerows(csv_content)
        benchmark_file = f.name

    # Deep copy input to avoid modification
    benchmark_file_copy = copy.deepcopy(benchmark_file)

    # Call func0 to verify input validity
    try:
        expected = load_benchmark_data(benchmark_file_copy)
    except Exception:
        os.unlink(benchmark_file)
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "benchmark_file": benchmark_file_copy
        }
    })

    # Clean up temporary file
    os.unlink(benchmark_file)

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)