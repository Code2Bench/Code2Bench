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
def validate_and_extract_accelerator_classifiers(classifiers: list) -> list:
    accelerator_classifiers = [c for c in classifiers if c.startswith("Environment ::")]
    if not accelerator_classifiers:
        return []

    accelerator_values = [c[len("Environment :: ") :] for c in accelerator_classifiers]

    valid_accelerators = {
        "GPU :: NVIDIA CUDA",
        "GPU :: AMD ROCm",
        "GPU :: Intel Arc",
        "NPU :: Huawei Ascend",
        "GPU :: Apple Metal",
    }

    for accelerator_value in accelerator_values:
        if accelerator_value not in valid_accelerators:
            return []

    return accelerator_values

# Strategy for generating classifiers
def classifier_strategy():
    valid_accelerators = [
        "Environment :: GPU :: NVIDIA CUDA",
        "Environment :: GPU :: AMD ROCm",
        "Environment :: GPU :: Intel Arc",
        "Environment :: NPU :: Huawei Ascend",
        "Environment :: GPU :: Apple Metal",
    ]
    return st.one_of([
        st.lists(st.sampled_from(valid_accelerators), min_size=1, max_size=5),
        st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50), min_size=0, max_size=5),
        st.lists(st.just("Environment :: Invalid Accelerator"), min_size=1, max_size=5),
        st.just([])
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(classifiers=classifier_strategy())
@example(classifiers=[])
@example(classifiers=["Environment :: GPU :: NVIDIA CUDA"])
@example(classifiers=["Environment :: GPU :: NVIDIA CUDA", "Environment :: GPU :: AMD ROCm"])
@example(classifiers=["Environment :: Invalid Accelerator"])
@example(classifiers=["Not an accelerator"])
def test_validate_and_extract_accelerator_classifiers(classifiers):
    global stop_collecting
    if stop_collecting:
        return
    
    classifiers_copy = copy.deepcopy(classifiers)
    try:
        expected = validate_and_extract_accelerator_classifiers(classifiers_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(c.startswith("Environment ::") for c in classifiers) or not classifiers:
        generated_cases.append({
            "Inputs": {"classifiers": classifiers},
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