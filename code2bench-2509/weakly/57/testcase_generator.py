from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from PIL import Image
from io import BytesIO
import base64
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
def image_to_data_url(image):
    buf = BytesIO()
    image.save(buf, format="PNG")
    b64_str = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64_str}"

# Strategy for generating PIL images
def image_strategy():
    return st.one_of(
        st.builds(
            Image.new,
            mode=st.just("RGB"),
            size=st.tuples(
                st.integers(min_value=1, max_value=100),
                st.integers(min_value=1, max_value=100)
            ),
            color=st.tuples(
                st.integers(min_value=0, max_value=255),
                st.integers(min_value=0, max_value=255),
                st.integers(min_value=0, max_value=255)
            )
        ),
        st.builds(
            Image.new,
            mode=st.just("L"),
            size=st.tuples(
                st.integers(min_value=1, max_value=100),
                st.integers(min_value=1, max_value=100)
            ),
            color=st.integers(min_value=0, max_value=255)
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(image=image_strategy())
@example(image=Image.new("RGB", (1, 1), (0, 0, 0)))
@example(image=Image.new("L", (1, 1), 255))
@example(image=Image.new("RGB", (10, 10), (255, 255, 255)))
def test_image_to_data_url(image):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    image_copy = copy.deepcopy(image)

    # Call func0 to verify input validity
    try:
        expected = image_to_data_url(image_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "image": {
                "mode": image_copy.mode,
                "size": image_copy.size,
                "color": image_copy.getpixel((0, 0)) if image_copy.size != (0, 0) else None
            }
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