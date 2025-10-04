from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(vectors)
    return similarity[0][1]

# Strategy for generating text inputs
def text_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=1, max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text1=text_strategy(), text2=text_strategy())
@example(text1="hello world", text2="hello world")
@example(text1="hello", text2="world")
@example(text1="", text2="")
@example(text1="hypothesis", text2="property-based testing")
@example(text1="12345", text2="67890")
def test_cosine_sim(text1: str, text2: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    text1_copy = copy.deepcopy(text1)
    text2_copy = copy.deepcopy(text2)

    # Call func0 to verify input validity
    try:
        similarity = cosine_sim(text1_copy, text2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text1": text1_copy,
            "text2": text2_copy
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