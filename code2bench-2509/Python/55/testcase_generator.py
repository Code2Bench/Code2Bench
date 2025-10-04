from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def get_gpu_num(model_name):
    model_name = model_name.lower()
    kws = {
        8: ['65b', '70b'],
        4: ['30b', '33b', '35b', '40b'],
        2: ['13b', '14b', '20b', '8b'],
        1: ['6b', '7b', 'moss'],
    }
    for k in [8, 4, 2, 1]:
        for keyword in kws[k]:
            if keyword in model_name:
                return k
    return 8

# Strategy for generating model names
def model_name_strategy():
    keywords = ['65b', '70b', '30b', '33b', '35b', '40b', '13b', '14b', '20b', '8b', '6b', '7b', 'moss']
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50).map(lambda x: x.lower()),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
            st.sampled_from(keywords),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
        ).map(lambda x: ''.join(x).lower()),
        st.sampled_from(keywords)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(model_name=model_name_strategy())
@example(model_name="65b")
@example(model_name="70b")
@example(model_name="30b")
@example(model_name="33b")
@example(model_name="35b")
@example(model_name="40b")
@example(model_name="13b")
@example(model_name="14b")
@example(model_name="20b")
@example(model_name="8b")
@example(model_name="6b")
@example(model_name="7b")
@example(model_name="moss")
@example(model_name="random_model_name")
def test_get_gpu_num(model_name):
    global stop_collecting
    if stop_collecting:
        return
    
    model_name_copy = copy.deepcopy(model_name)
    try:
        expected = get_gpu_num(model_name_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"model_name": model_name},
        "Expected": expected
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)