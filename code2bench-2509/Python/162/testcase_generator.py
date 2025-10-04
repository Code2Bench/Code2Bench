from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Any, Dict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def parse_prompt_line(line: str) -> Dict[str, Any]:
    parts = line.split(" --")
    prompt = parts[0].strip()

    # Create dictionary of overrides
    overrides = {"prompt": prompt}

    for part in parts[1:]:
        if not part.strip():
            continue
        option_parts = part.split(" ", 1)
        option = option_parts[0].strip()
        value = option_parts[1].strip() if len(option_parts) > 1 else ""

        # Map options to argument names
        if option == "w":
            overrides["image_size_width"] = int(value)
        elif option == "h":
            overrides["image_size_height"] = int(value)
        elif option == "d":
            overrides["seed"] = int(value)
        elif option == "s":
            overrides["infer_steps"] = int(value)
        elif option == "fs":
            overrides["flow_shift"] = float(value)
        elif option == "i":
            overrides["image_path"] = value
        elif option == "ci":  # control_image_path
            overrides["control_image_path"] = value

    return overrides

# Strategy for generating prompt lines
def prompt_line_strategy():
    prompt = st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    options = st.lists(
        st.one_of([
            st.tuples(st.just("w"), st.integers(min_value=1, max_value=2147483647)),
            st.tuples(st.just("h"), st.integers(min_value=1, max_value=2147483647)),
            st.tuples(st.just("d"), st.integers(min_value=0, max_value=2147483647)),
            st.tuples(st.just("s"), st.integers(min_value=1, max_value=2147483647)),
            st.tuples(st.just("fs"), st.floats(allow_nan=False, allow_infinity=False, width=32)),
            st.tuples(st.just("i"), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)),
            st.tuples(st.just("ci"), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)),
        ]),
        max_size=10
    )
    return st.tuples(prompt, options).map(lambda x: x[0] + " --" + " --".join(f"{opt} {val}" for opt, val in x[1]))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(line=prompt_line_strategy())
@example(line="prompt")
@example(line="prompt --w 512 --h 512")
@example(line="prompt --d 42 --s 50")
@example(line="prompt --fs 0.5")
@example(line="prompt --i image.png")
@example(line="prompt --ci control_image.png")
def test_parse_prompt_line(line: str):
    global stop_collecting
    if stop_collecting:
        return
    
    line_copy = copy.deepcopy(line)
    try:
        expected = parse_prompt_line(line_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"line": line},
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