from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import re
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
def parse_web_response(response):
    pattern = r"Thought:|Action:|Memory_Updated:"
    answer = re.findall(r"<answer>(.*?)</answer>", response, re.DOTALL)
    if not answer:
        return None

    response_split = re.split(pattern, answer[0])
    if len(response_split) < 4:
        return None

    thought = response_split[1].strip()
    action = response_split[2].strip()
    memory_str = response_split[3].strip()

    memory = {}
    if memory_str:
        memory = json.loads(memory_str)

    return {"thought": thought, "action": action, "memory": memory}

# Strategies for generating inputs
def response_strategy():
    # Generate valid JSON for memory
    memory_strategy = st.recursive(
        st.one_of(
            st.none(),
            st.booleans(),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
        ),
        lambda children: st.lists(children, min_size=0, max_size=3) | st.dictionaries(st.text(), children, max_size=3),
        max_leaves=5
    ).map(lambda x: json.dumps(x))

    # Generate thought, action, and memory strings
    thought_strategy = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    action_strategy = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

    # Combine into a valid response string
    return st.builds(
        lambda t, a, m: f"<answer>Thought: {t}\nAction: {a}\nMemory_Updated: {m}</answer>",
        thought_strategy, action_strategy, memory_strategy
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(response=response_strategy())
@example(response="<answer>Thought: Think\nAction: Act\nMemory_Updated: {}</answer>")
@example(response="<answer>Thought: Think\nAction: Act\nMemory_Updated: {\"key\": \"value\"}</answer>")
@example(response="<answer>Thought: Think\nAction: Act\nMemory_Updated: null</answer>")
@example(response="<answer>Thought: Think\nAction: Act\nMemory_Updated: </answer>")
@example(response="<answer>Thought: Think\nAction: Act</answer>")
@example(response="<answer>Thought: Think</answer>")
@example(response="<answer></answer>")
@example(response="invalid response")
def test_parse_web_response(response: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    response_copy = copy.deepcopy(response)

    # Call func0 to verify input validity
    try:
        result = parse_web_response(response_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "response": response_copy
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