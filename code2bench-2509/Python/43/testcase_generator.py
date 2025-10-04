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
def to_data_url(image_str: str) -> str:
    if not isinstance(image_str, str) or not image_str:
        return image_str
    s = image_str.strip()
    if s.startswith("data:image/"):
        return s
    if s.startswith("http://") or s.startswith("https://"):
        return s
    b64 = s.replace("\n", "").replace("\r", "")
    kind = "image/png"
    if b64.startswith("/9j/"):
        kind = "image/jpeg"
    elif b64.startswith("iVBORw0KGgo"):
        kind = "image/png"
    elif b64.startswith("R0lGOD"):
        kind = "image/gif"
    return f"data:{kind};base64,{b64}"

# Strategy for generating image strings
def image_strategy():
    return st.one_of([
        # Empty string
        st.just(""),
        # Non-string inputs
        st.one_of([st.integers(), st.floats(), st.booleans(), st.none()]).map(str),
        # Data URL
        st.tuples(
            st.just("data:image/"),
            st.one_of([st.just("png"), st.just("jpeg"), st.just("gif")]),
            st.just(";base64,"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
        ).map(lambda x: "".join(x)),
        # HTTP URL
        st.tuples(
            st.one_of([st.just("http://"), st.just("https://")]),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
        ).map(lambda x: "".join(x)),
        # Base64 encoded images
        st.one_of([
            st.tuples(
                st.just("/9j/"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
            ).map(lambda x: "".join(x)),
            st.tuples(
                st.just("iVBORw0KGgo"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
            ).map(lambda x: "".join(x)),
            st.tuples(
                st.just("R0lGOD"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
            ).map(lambda x: "".join(x)),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
        ])
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(image_str=image_strategy())
@example(image_str="")
@example(image_str="data:image/png;base64,iVBORw0KGgo")
@example(image_str="http://example.com/image.png")
@example(image_str="https://example.com/image.png")
@example(image_str="/9j/abc123")
@example(image_str="iVBORw0KGgoabc123")
@example(image_str="R0lGODabc123")
@example(image_str="randomstring")
def test_to_data_url(image_str):
    global stop_collecting
    if stop_collecting:
        return
    
    image_str_copy = copy.deepcopy(image_str)
    try:
        expected = to_data_url(image_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"image_str": image_str},
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